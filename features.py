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
