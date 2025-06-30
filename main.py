import os
import sys
import dotenv
import argparse


def main():
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser(
        description="YATCH (yet another Trello CLI, homies)")
    parser.add_argument("-v", "--version",
                        action="store_true", help="Show version")

    # if nothing, help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    args.func(args)
