import sqlite3

DATABASE_PATH = './database/database.db'
SCRIPT_PATH = './database/db_schema.sql'

def touch_database():
    with open(SCRIPT_PATH, 'r') as sql_file:
        sql_script = sql_file.read()

    conn = setup_connection()
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    close_connection(conn)


def setup_connection():
    return sqlite3.connect(DATABASE_PATH)


def close_connection(conn):
    conn.close()


def check_if_exists(table_name, where_column_name, sanitised_value):
    conn = setup_connection()
    cursor = conn.cursor()

    task = (sanitised_value,)
    cursor.execute(
        f'SELECT * FROM {table_name} WHERE {where_column_name}=?', task)

    row = cursor.fetchone()
    close_connection(conn)

    if row is None:
        return False
    else:
        return True


def get_first_row(table_name, columns, where_column_name, sanitised_value):
    conn = setup_connection()
    cursor = conn.cursor()

    if where_column_name is not None:
        task = (sanitised_value,)
        cursor.execute(
            f'SELECT {columns} FROM {table_name} WHERE {where_column_name}=?', task)
    else:
        cursor.execute(f'SELECT {columns} FROM {table_name}')

    row = cursor.fetchone()
    close_connection(conn)

    return row


def get_all_rows(table_name, columns, where_column_name, sanitised_value):
    conn = setup_connection()
    cursor = conn.cursor()

    if where_column_name is not None:
        task = (sanitised_value,)
        cursor.execute(
            f'SELECT {columns} FROM {table_name} WHERE {where_column_name}=?', task)
    else:
        cursor.execute(f'SELECT {columns} FROM {table_name}')

    rows = cursor.fetchall()
    close_connection(conn)

    return rows
