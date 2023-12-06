import sqlite3


def connect_to_db():
    database = sqlite3.connect("data.sqlite")
    cursor = database.cursor()
    return cursor, database
