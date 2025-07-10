import datetime
import json
import os
import dotenv
import sqlite3
from utils import *

# GENERAL


def setup(args, key=None, value=None):
    if args.command == "setup":
        key = input("Trello Key: ")
        token = input("Trello token: ")
        if len(key) < 1:
            raise ("Need to provide key")
        if len(token) < 1:
            raise ("Need to provide token")

    env = dict()

    with open(".env", "r+") as e:
        variables = e.readlines()
        for var in variables:
            k, v = var.split("=")
            env[k] = v
        
        if key and value:
            env[key] = value
        if args.command == "setup":
            env["API_KEY"] = key
            env["API_TOKEN"] = token

        e.seek(0)
        e.truncate()
        for k, v in env.items():
            e.writelines(k+"="+v.removesuffix("\n")+"\n")
    
    dotenv.load_dotenv()
    print("Enviroment updated")

    if args.command == "setup":
        try:
            conn = sqlite3.connect('db.db')
            conn.close()
            print("Local DB connection working")
        except Exception as e:
            raise (e)

    return


def refresh(args):
    board_refresh(drill=True)
    return

def board_processor(args):
    print(args)
    if args.list: board_list()
    if args.update: board_update(args)

def board_refresh(board_id=None, drill=False):
    print("Fetching Boards...")
    board_list = []
    json_data = api("GET", "/1/members/me/boards")

    print("Saving Boards..")
    query = """
    insert into boards(id, name, desc, closed, dateClosed, url)
    values(?,?,?,?,?,?)
    """
    if board_id:
        json_data = [board for board in json_data if board.get("id")==board_id]
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        for board in json_data:
            try:
                cursor.execute(
                    query,(
                        board.get("name"),
                        board.get("desc"),
                        board.get("closed"),
                        board.get("dateClosed"),
                        board.get("url"),
                        board.get("id"),
                    )
                )
            except sqlite3.IntegrityError:
                cursor.execute("""
                update boards
                set 
                    name = ?,
                    desc = ?,
                    closed = ?,
                    dateClosed = ?,
                    url = ?
                where id = ?
                """,(
                        board.get("name"),
                        board.get("desc"),
                        board.get("closed"),
                        board.get("dateClosed"),
                        board.get("url"),
                        board.get("id"),
                    ))
            if not board.get("closed"):
                board_list.append([board.get("id"), board.get("name")])
    print("Boards saved successfully!")
    if drill:
        print(f"Fetching details for board {board_id}")
        members_refresh(board_list)
        list_refresh(board_list)
        cards_refresh(board_list, drill)



def get_boards():
    query = """ select * from boards """
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    
    return data

def board_list(data=None):
    if not data: 
        data = get_boards()
    for index, board in enumerate(data):
        print(f'{index:3d} | {board[1][:30]:30} | {board[2][:45]:45} | Closed:{board[3]}')
    return

def board_default(args):
    boards = get_boards()

    if args.show:
        for index, board in enumerate(boards):
            print(f'{index:3d} | {board[1][:30]:30} | {board[2][:45]:45} | Closed:{board[3]}')
    if args.change:
        print("Available Boards:")
        board_list(boards)
        index = int(input("Choose default board (index): "))
        
        setup(args,"DEFAULT_BOARD", boards[index][0])

def board_update(args):
    board_id = os.getenv("DEFAULT_BOARD")

    if not args.default:
        boards = get_boards()
        print("Available Boards:")
        board_list(boards)
        index = int(input("Choose board to update (index): "))
        board_id = boards[index].get(id)
    
    board_refresh(board_id, True)

# LIST

def list_default(args):
    board_list = [os.getenv("DEFAULT_BOARD")]
    if args.all:
        bs = get_boards()
        board_list = [b[0] for b in bs]

    lists = get_list(board_list)

    if args.show:
        list_list(lists)
    if args.change:
        print("Available lists:")
        list_list(lists)
        index = int(input("Choose default list (index): "))
        
        setup(args,"DEFAULT_LIST", lists[index][0])


def list_refresh(board_list=[]):
    for board in board_list:
        print("Fetching Lists...")
        json_data = api("GET", f"/1/boards/{board}/lists")
        print("Saving Lists..")

        query = """
        insert into lists(idBoard, id, name, closed)
        values(?,?,?,?)
        """
        with sqlite3.connect('db.db') as conn:
            cursor = conn.cursor()
            for card_list in json_data:
                try:
                    cursor.execute(
                        query,(
                        board,
                        card_list.get("id"),
                        card_list.get("name"),
                        card_list.get("closed"),)
                    )
                except sqlite3.IntegrityError as e:
                    if e == "UNIQUE constraint failed: lists.idBoard, lists.id":
                        cursor.execute("""
                        update lists
                            set 
                                name = ?,
                                closed = ?
                        where 
                            id = ?
                            and idBoard = ?
                        """,(
                            card_list.get("name"),
                            card_list.get("closed"),
                            card_list.get("id"),
                            board,
                        ))
        print("Lists saved successfully!")

def get_list(board_list=[]):
    if len(board_list) == 0:
        board_list = [os.getenv("DEFAULT_BOARD")]
    query = """
    select 
        l.idBoard,
        l.id,
        l.name,
        l.closed,
        b.name as board
    from lists l
    join boards b on b.id = l.idBoard 
    where b.id in (%s)
    """
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query %','.join('?'*len(board_list)),  board_list)
        data = cursor.fetchall()
    
    return data

def list_get_cards(list_list):
    query = """
    select 
        l.idBoard,
        c.idList,
        c.id,
        c.name,
        c.desc,
        c.due,
        c.close,
        c.dateLasActivity,
        c.labels,
        l.name list
        b.name as board
    from cards c
    join lists l on c.idList = l.id
    join boards b on b.id = l.idBoard 
    where c.idList in (%s)
    """
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query%','.join('?'*len(list_list)),list_list)
        data = cursor.fetchall()
    
    return data

def list_processor(args):
    board_list = [os.getenv("DEFAULT_BOARD")]
    if args.update:
        cards_refresh(board_list)
    
    if args.all:
        boards = get_boards()
        board_list = [b[0] for b in boards]
    list_list = get_list(board_list)
    
    if not args.wide:
        default_list = os.getenv("DEFAULT_LIST")
        if default_list != "":
            list_list = [l for l in list_list if l[1]==default_list]

    if args.cards:
        list_all_cards(list_get_cards(list_list))


def list_list(data=None):
    if not data: 
        bs = get_boards()
        board_list = [b[0] for b in bs]
        data = get_list(board_list)
    for index, l in enumerate(data):
        print(f'{index:3d} | List:{l[2][:30]:30} | Board:{l[4][:30]:30} | Closed:{l[3]}')
    return

def list_all_cards(data=[]):
    if not data: 
        data = list_get_cards([os.getenv("DEFAULT_LIST")])
    for index, c in enumerate(data):
        print("|"+"-"*29+f"{index}"+"-"*30+"|")
        print("|"+f"{c[3][:60]:60}"+"|")
        print("|"+f"{c[4][:60]:60}"+"|")
        print("|"+f"Due: {c[4]:30} Closed: {c[5]:17}"+"|")
        print("|"+f"Last: {c[5]:54}"+"|")
        print("|"+f"{c[6]:60}"+"|")
        print("|"+f"List: {c[7]:23} Board: {c[8]:23}"+"|")
        print("|"+"-"*60+"|")
    return



def list_add(args):
    return


def list_move(args):
    return


def list_remove(args):
    return


# CARD



def cards_refresh(board_list=[], drill=False):
    card_list = []
    for board in board_list:
        print("Fetching Cards...")
        json_data = api("GET", f"/1/boards/{board}/cards")

        print("Saving Cards..")

        query = """
        insert into cards(idList,id,name,desc,due,closed,dateLastActivity,labels,url)
        values(?,?,?,?,?,?,?,?,?)
        """
        with sqlite3.connect('db.db') as conn:
            cursor = conn.cursor()
            for card in json_data:
                cursor.execute(
                    query,(
                    card.get("idList"),
                    card.get("id"),
                    card.get("name"),
                    card.get("desc"),
                    card.get("due"),
                    card.get("closed"),
                    card.get("dateLastActivity"),
                    "|".join([label.get("name") for label in card.get("labels")]),
                    card.get("url"))
                )
    if drill:
        comments_refresh(card_list)
    print("Cards saved successfully!")


def card_add(args):
    return


def card_move(args):
    return


def card_delete(args):
    return


def card_comment_on(args):
    return


def card_edit_description(args):
    return


def card_set_due_date(args):
    return


def checklist_add(args):
    return


def checklist_add_to(args):
    return


def checklist_remove_from(args):
    return


def checklist_flip_check_from(args):
    return


def comments_refresh(card_list=[]):
    for card in card_list:
        print(f"Fetching comments for card {card}")
        comments = api("GET", f"/1/cards/{card.get('id')}/actions?filter=commentCard")
        with sqlite3.connect('db.db') as conn:
            cursor = conn.cursor() 
            for c in comments:
                cursor.execute(
                    """
                    insert into comments (id,idCard,idMemberCreator,text,date)
                    values (?,?,?,?,?)
                    """,(
                    c.get("id"),
                    c.get("data").get("card").get("id"),
                    c.get("idMemberCreator"),
                    c.get("data").get("text"),
                    c.get("date"))
                )
        print("Comments saved successfully!")

def members_refresh(board_list=[]):
    for board in board_list:
        print("Fetching Board members for {board}...")
        json_data = api("GET", f"/1/boards/{board}/members")
        print("Saving Board members..")

        query = """
        insert into members(idBoard, id, fullName, userName)
        values(?,?,?,?)
        """
        with sqlite3.connect('db.db') as conn:
            cursor = conn.cursor()
            for member in json_data:
                try:
                    cursor.execute(
                        query,(
                        board,
                        member.get("id"),
                        member.get("fullName"),
                        member.get("userName"))
                    )
                except sqlite3.IntegrityError:
                    continue #dont care enough to update names
        print("Board members saved successfully!")
