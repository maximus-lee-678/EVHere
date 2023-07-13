import sqlite3
import csv
import sys

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


def safe_select(query, task, get_type):
    """
    (SELECT) Wrapper that ensures OperationalErrors do not cause execution termination. \n
    task must be specified:\n
    \t>> (Tuple), None\n
    get_type must be specified:\n
    \t>> 'one', 'all'\n
    Returns Dictionary with keys:\n
    <select_successful> True or False.\n
    <num_rows> (if <select_successful> is True) =Value= Number of rows returned.\n
    <content> (if <select_successful> is True) Content. (can be blank)\n
    courtesy of: https://stackoverflow.com/questions/25371636/how-to-get-sqlite-result-error-codes-in-python
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        if task:
            cursor.execute(query, task)
        else:
            cursor.execute(query)

        if get_type == 'one':
            content = cursor.fetchone()
            return_dict = {'select_successful': True,
                           'num_rows': 0 if content is None else 1,
                           'content': content}

        elif get_type == 'all':
            content = cursor.fetchall()
            return_dict = {'select_successful': True,
                           'num_rows': len(content),
                           'content': content}

        else:
            return_dict = {'select_successful': False}

        # print('Query is: %s' % query, file=sys.stderr)
    except sqlite3.Error as err:
        print('SQLite error: %s' % (' '.join(err.args)), file=sys.stderr)
        print('Exception class is: %s' % err.__class__, file=sys.stderr)
        # print('Query is: %s' % query, file=sys.stderr)

        return_dict = {'select_successful': False}

    finally:
        conn.close()
        return return_dict


def safe_transaction(query, task):
    """
    (CREATE, UPDATE, DELETE) Wrapper that ensures OperationalErrors do not cause execution termination. \n
    task must be specified:\n
    \t>> (Tuple), None\n
    Returns Dictionary with keys:\n
    <transaction_successful> True or False.\n
    <rows_affected> (if <select_successful> is True) =Value= Number of rows affected.\n
    courtesy of: https://stackoverflow.com/questions/25371636/how-to-get-sqlite-result-error-codes-in-python
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        if task:
            cursor.execute(query, task)
        else:
            cursor.execute(query)

        conn.commit()

        return_dict = {'transaction_successful': True,
                       'rows_affected': cursor.execute('SELECT changes()').fetchone()[0]}

    except sqlite3.OperationalError as err:
        print('SQLite error: %s' % (' '.join(err.args)), file=sys.stderr)
        print('Exception class is: %s' % err.__class__, file=sys.stderr)
        print('Query is: %s' % query, file=sys.stderr)
        
        return_dict = {'transaction_successful': False}

    finally:
        conn.close()
        return return_dict
