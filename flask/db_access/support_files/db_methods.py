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
    | Automatically called by server when database does not exist.\n
    | Sets up schema and populates tables.
    """

    # Read schema
    with open(SCRIPT_PATH, 'r') as sql_file:
        sql_script = sql_file.read()

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Write schema to database
    cursor.executescript(sql_script)

    # Read charger data, write to variable
    with open(DEFAULT_CHARGER_PATH, 'r', encoding='UTF-8') as file:
        # csv.DictReader uses first line in file for column headings by default
        dict_reader = csv.DictReader(file)  # comma is default delimiter
        to_db = [(i['id'], i['name'], i['latitude'], i['longitude'], i['address'], i['currently_open'],
                  i['pv_current_in'], i['pv_energy_level'], i['rate_current'], i['rate_predicted'], i['active'], i['last_updated']) for i in dict_reader]

    # Write charger details to database
    cursor.executemany(
        "INSERT INTO charger VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", to_db)

    # Read connector data, write to variable
    with open(DEFAULT_CONNECTOR_PATH, 'r', encoding='UTF-8') as file:
        # csv.DictReader uses first line in file for column headings by default
        dict_reader = csv.DictReader(file)  # comma is default delimiter
        to_db = [(i['id'], i['current_type'], i['name_connector'],
                  i['output_voltage_max'], i['output_current_max']) for i in dict_reader]

    # Write connector details to database
    cursor.executemany("INSERT INTO connector_type VALUES (?,?,?,?,?)", to_db)

    # Read charger connector data, write to variable
    with open(DEFAULT_CHARGER_CONNECTORS_PATH, 'r', encoding='UTF-8') as file:
        # csv.DictReader uses first line in file for column headings by default
        dict_reader = csv.DictReader(file)  # comma is default delimiter
        to_db = [(i['id'], i['id_charger'], i['id_connector_type'], i['in_use'], i['output_voltage'], i['output_current'])
                 for i in dict_reader]

    # Write connector details to database
    cursor.executemany(
        "INSERT INTO charger_available_connector VALUES (?,?,?,?,?,?)", to_db)

    conn.commit()
    conn.close()


def safe_select(query, task, get_type):
    """
    | SELECT sqlite Wrapper.

    :param string query: query string
    :param tuple/bool task: tuple containing fields for prepared statement, or None
    :param string get_type: 'one' or 'all'

    :returns: Dictionary
    :key 'select_successful': True or False.
    :key 'num_rows': (int) *('select_successful' == True)* Number of rows returned.
    :key 'content': (array) *('select_successful' == True)* Output array. May be empty.
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
    | CREATE, UPDATE, DELETE sqlite Wrapper.

    :param string query: query string
    :param tuple/bool task: tuple containing fields for prepared statement, or None

    :returns: Dictionary
    :key 'transaction_successful': True or False.
    :key 'rows_affected': (int) *('transaction_successful' == True)* Number of rows affected.
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
        print('return dict {}'.format(return_dict))
    except sqlite3.OperationalError as err:
        print('SQLite error: %s' % (' '.join(err.args)), file=sys.stderr)
        print('Exception class is: %s' % err.__class__, file=sys.stderr)
        print('Query is: %s' % query, file=sys.stderr)

        return_dict = {'transaction_successful': False}

    finally:
        conn.close()
        return return_dict
