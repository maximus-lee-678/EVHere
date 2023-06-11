import helper_functions

import db_methods

CONNECTOR_FOUND = 100
CONNECTOR_NOT_FOUND = 101

service_code_dict = {
    CONNECTOR_FOUND: "Found connectors.",
    CONNECTOR_NOT_FOUND: "No matching connectors found."
}


def get_all_connectors():
    """
    Retrieves ALL connectors from database.\n
    Returns Dictionary with keys:\n
    <result> CONNECTOR_NOT_FOUND or CONNECTOR_FOUND.\n
    <content> (if <result> is CONNECTOR_FOUND) Dictionary containing connector information.
    """

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT name_short, name_long, name_connector FROM connector_type')

    rows = cursor.fetchall()
    db_methods.close_connection(conn)

    if db_methods.check_fetchall_has_nothing(rows):
        return {'result': CONNECTOR_NOT_FOUND}

    key_values = []
    # transforming array to key-values
    for row in rows:
        key_values.append(
            {"name_short": row[0], "name_long": row[1], "name_connector": row[2]})

    return {'result': CONNECTOR_FOUND, 'content': key_values}


def get_connector_id_by_name_short(input_name_short):
    """
    Retrieves a single connector's id based on name from database.\n
    Returns Dictionary with keys:\n
    <result> CONNECTOR_NOT_FOUND or CONNECTOR_FOUND.\n
    <content> (if <result> is CONNECTOR_FOUND) Value containing connector ID.
    """

    # sanitise name_short
    name_short = helper_functions.string_sanitise(input_name_short)

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    task = (name_short,)
    cursor.execute('SELECT id FROM connector_type WHERE name_short=?', task)

    row = cursor.fetchone()
    db_methods.close_connection(conn)

    if db_methods.check_fetchone_has_nothing(row):
        return {'result': CONNECTOR_NOT_FOUND}

    return {'result': CONNECTOR_FOUND, 'content': row[0]}
