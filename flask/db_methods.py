import sqlite3
import csv

DATABASE_PATH = './database/database.db'
SCRIPT_PATH = './database/db_schema.sql'
DEFAULT_CHARGER_PATH = './database/chargers_modded.csv'
DEFAULT_CONNECTOR_PATH = './database/connectors_modded.csv'
DEFAULT_CHARGER_CONNECTORS_PATH = './database/chargers_connectors_modded.csv'


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
        dict_reader = csv.DictReader(file)  # comma is default delimiter
        to_db = [(i['id'], i['name'], i['latitude'], i['longitude'], i['address'], i['provider'],
                  i['connectors'], i['online'], i['kilowatts'], i['twenty_four_hours'], i['last_updated']) for i in dict_reader]

    # Write charger details to database
    cursor.executemany(
        "INSERT INTO charger VALUES (?,?,?,?,?,?,?,?,?,?,?)", to_db)

    # Read connector data, write to variable
    with open(DEFAULT_CONNECTOR_PATH, 'r', encoding='UTF-8') as file:
        # csv.DictReader uses first line in file for column headings by default
        dict_reader = csv.DictReader(file)  # comma is default delimiter
        to_db = [(i['id'], i['name_short'], i['name_long'],
                  i['name_connector']) for i in dict_reader]

    # Write connector details to database
    cursor.executemany("INSERT INTO connector_type VALUES (?,?,?,?)", to_db)

    # Read charger connector data, write to variable
    with open(DEFAULT_CHARGER_CONNECTORS_PATH, 'r', encoding='UTF-8') as file:
        # csv.DictReader uses first line in file for column headings by default
        dict_reader = csv.DictReader(file)  # comma is default delimiter
        to_db = [(i['id'], i['id_charger'], i['id_connector_type'])
                 for i in dict_reader]

    # Write connector details to database
    cursor.executemany(
        "INSERT INTO charger_available_connector VALUES (?,?,?)", to_db)

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


def check_fetchall_has_nothing(rows):
    """
    Helper that checks if a fetchall returned nothing.
    """

    return len(rows) == 0


def check_fetchone_has_nothing(row):
    """
    Helper that checks if a fetchone returned nothing.
    """

    return row is None
