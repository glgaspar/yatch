import datetime
import json
import os
import dotenv
import sqlite3
from utils import *

# GENERAL
def setup():
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

        env["API_KEY"] = key+"\n"
        env["API_TOKEN"] = token+"\n"

        e.seek(0)
        e.truncate()
        for k, v in env.items():
            e.writelines(k+"="+v)

    print("Credentials updated")

    try:
        conn = sqlite3.connect('my_database.db')
        conn.close()
        print("Local DB connection working")
    except Exception as e:
        raise (e)

    return


def refresh():
    board_list = []
    print("Fetching Boards...")
    json_data = api("GET", "/members/me/boards")
    
    print("Saving Boards..")
    query = """
    insert into boards(id, name, desc, closed, dateClosed, url)
    values(?,?,?,?,?,?)
    """
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        for board in json_data:
            cursor.execute(
                query, 
                board.get("id"), 
                board.get("name"), 
                board.get("desc"), 
                board.get("closed"), 
                board.get("dateClosed"), 
                board.get("url")
            )
        if not board.get("closed"):
            board_list.append(board.get("id"),board.get("name"))
    print("Boards saved successfully!")

    for board in board_list:
        print(f"Fetching details for board {board[1]}")

        print("Fetching Board members...")
        json_data = api("GET", f"/boards/{board[0]}/members")
        print("Saving Board members..")

        query = """
        insert into members(idBoard, id, fullName, userName)
        values(?,?,?,?)
        """
        with sqlite3.connect('db.db') as conn:
            cursor = conn.cursor()
            for member in json_data:
                cursor.execute(
                    query, 
                    board[0],
                    member.get("id"), 
                    member.get("fullName"), 
                    member.get("userName") 
                )
        print("Board members saved successfully!")
        
        print("Fetching Lists...")
        json_data = api("GET", f"/boards/{board[0]}/lists")
        print("Saving Lists..")

        query = """
        insert into lists(idBoard, id, name, closed)
        values(?,?,?,?)
        """
        with sqlite3.connect('db.db') as conn:
            cursor = conn.cursor()
            for card_list in json_data:
                cursor.execute(
                    query, 
                    board[0],
                    card_list.get("id"), 
                    card_list.get("name"), 
                    card_list.get("closed"), 
                )
        print("Lists saved successfully!")
        
        print("Fetching Cards...")
        json_data = api("GET", f"/boards/{board[0]}/members")

        print("Saving Cards..")

        query = """
        insert into cards(idList,id,name,desc,due,closed,dateLastActivity,labels,url)
        values(?,?,?,?,?,?,?,?,?)
        """
        with sqlite3.connect('db.db') as conn:
            cursor = conn.cursor()
            for card in json_data:
                cursor.execute(
                    query, 
                    card.get("idList"),
                    card.get("id"),
                    card.get("name"),
                    card.get("desc"),
                    card.get("due"),
                    card.get("closed"),
                    card.get("dateLastActivity"),
                    card.get("labels"),
                    card.get("url")
                )
            
            comments = api("GET", f"/cards/{card.get(id)}/actions?filter=commentCard")
            for c in comments:
                cursor.execute(
                    """
                    insert into comments (id,idCard,idMemberCreator,text,data)
                    values (?,?,?,?)
                    """,
                    c.get("id"),
                    c.get("data").get("card").get("id"),
                    c.get("idMemberCreator"),
                    c.get("data").get("text"),
                    c.get("date")
                )
        print("Cards saved successfully!")
    
    return


def board_list():

    return


def list_all_card():
    return

# CARD


def card_add():
    return


def card_move():
    return


def card_delete():
    return


def card_comment_on():
    return


def card_edit_description():
    return


def card_set_due_date():
    return


def checklist_add():
    return


def checklist_add_to():
    return


def checklist_remove_from():
    return


def checklist_flip_check_from():
    return

# LIST


def list_add():
    return


def list_move():
    return


def list_remove():
    return
