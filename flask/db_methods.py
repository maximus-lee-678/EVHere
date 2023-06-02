import sqlite3
import csv

DATABASE_PATH = './database/database.db'
SCRIPT_PATH = './database/db_schema.sql'
DEFAULT_CHARGER_PATH = './database/chargers.csv'


def touch_database():
    """
    Called by server when database has been determined to not exist.\n
    Sets up schema and populates charger table.
    """

    # Read schema
    with open(SCRIPT_PATH, 'r') as sql_file:
        sql_script = sql_file.read()

    conn = setup_connection()
    cursor = conn.cursor()

    # Write schema to database
    cursor.executescript(sql_script)

    # Read charger data, write to variable
    with open(DEFAULT_CHARGER_PATH, 'r', encoding='UTF-8') as file:
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(file)  # comma is default delimiter
        to_db = [(i['id'], i['name'], i['latitude'], i['longitude'], i['address'], i['provider'],
                  i['connectors'], i['online'], i['kilowatts'], i['twenty_four_hours'], i['last_updated']) for i in dr]

    # Write charger details to database
    cursor.executemany(
        "INSERT INTO charger VALUES (?,?,?,?,?,?,?,?,?,?,?)", to_db)

    conn.commit()
    close_connection(conn)


def setup_connection():
    """
    Helper that returns a sqlite3 connection object.\n
    Remember to call close_connection(<variable>) when done.
    """
    return sqlite3.connect(DATABASE_PATH)


def close_connection(conn):
    """
    Helper that closes a sqlite3 connection object.\n
    Called on object returned by setup_connection().
    """
    conn.close()
