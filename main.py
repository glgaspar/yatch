import os
import sys
import dotenv
import argparse
from features import *

def main():
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser(description="YATCH (yet another Trello CLI, homies)")
    subparsers = parser.add_subparsers(dest="command")     

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

    setup_subparser = subparsers.add_parser("setup", help="Setup env")
    setup_subparser.set_defaults(func=setup)


    # if nothing, help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()