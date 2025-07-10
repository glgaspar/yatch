import os
import sys
import dotenv
import argparse
from features import *

def main():
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser(description="YATCH (yet another Trello CLI, homies)")
    subparsers = parser.add_subparsers(dest="command")     

    setup_subparser = subparsers.add_parser("setup", help="Setup env")
    setup_subparser.set_defaults(func=setup)

    refresh_subparser = subparsers.add_parser("refresh", help="Update all the data")
    refresh_subparser.set_defaults(func=refresh)

    boards_parser = subparsers.add_parser("boards", help="Show board data")
    boards_parser.set_defaults(func=board_processor)
    boards_parser.add_argument("-l", "--list", action="store_true", help="Show all boards")
    boards_parser.add_argument("-u", "--update", action="store_true", help="Update boards")
    boards_parser.add_argument("-d", "--default", action="store_true", help="Operate on default board")
    boards_subparser  = boards_parser.add_subparsers(dest="board")
    
    boards_default_parser = boards_subparser.add_parser("default", help="Show or define default board")
    boards_default_parser.set_defaults(func=board_default)
    boards_default_parser.add_argument("-s", "--show", action="store_true", help="Show default board")
    boards_default_parser.add_argument("-c", "--change", action="store_true", help="Change default board")

    list_parser = subparsers.add_parser("lists", help="Show list data")
    list_parser.set_defaults(func=list_processor)
    list_parser.add_argument("-a", "--all", action="store_true", help="Operates on all boards, otherwise operate only on default board")
    list_parser.add_argument("-u", "--update", action="store_true", help="Update lists and cards before operation")
    list_parser.add_argument("-w", "--wide", action="store_true", help="Operate on all Lists on default board, otherwise operate only on default list. If there is no default list, defaults to wide")
    list_parser.add_argument("-c", "--cards", action="store_true", help="Get all cards in a list")
    list_subparser = list_parser.add_subparsers(dest="list")

    list_default_parser = list_subparser.add_parser("default", help="Show or define default list")
    list_default_parser.set_defaults(func=list_default)
    list_default_parser.add_argument("-s", "--show", action="store_true", help="Show default list")
    list_default_parser.add_argument("-a", "--all", action="store_true", help="Operates on all boards, otherwise operate only on default board")
    list_default_parser.add_argument("-u", "--update", action="store_true", help="Update lists and cards before operation")
    list_default_parser.add_argument("-c", "--change", action="store_true", help="Change default list")

    # if nothing, help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()