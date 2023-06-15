# Universal imports
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods

# Other db_access imports
#


def get_all_connectors():
    """
    Retrieves ALL connectors from database.\n
    Returns Dictionary with keys:\n
    <result> CONNECTOR_NOT_FOUND or CONNECTOR_FOUND.\n
    <content> (if <result> is CONNECTOR_FOUND) [{Dictionary Array}] containing connector information.\n
    \t"keys":\n
    \t{"id", "name_short", "name_long", "name_connector"}
    """

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id, name_short, name_long, name_connector FROM connector_type')

    rows = cursor.fetchall()
    db_methods.close_connection(conn)

    if db_methods.check_fetchall_has_nothing(rows):
        return {'result': db_service_code_master.CONNECTOR_NOT_FOUND}

    key_values = []
    # transforming array to key-values
    for row in rows:
        key_values.append(
            {"id": row[0], "name_short": row[1], "name_long": row[2], "name_connector": row[3]})

    return {'result': db_service_code_master.CONNECTOR_FOUND, 'content': key_values}


def get_connector_id_by_name_short(input_name_short):
    """
    Retrieves a single connector's id based on name from database.\n
    Returns Dictionary with keys:\n
    <result> CONNECTOR_NOT_FOUND or CONNECTOR_FOUND.\n
    <content> (if <result> is CONNECTOR_FOUND) =Value= containing connector ID.
    """

    # sanitise name_short
    name_short = db_helper_functions.string_sanitise(input_name_short)

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    task = (name_short,)
    cursor.execute('SELECT id FROM connector_type WHERE name_short=?', task)

    row = cursor.fetchone()
    db_methods.close_connection(conn)

    if db_methods.check_fetchone_has_nothing(row):
        return {'result': db_service_code_master.CONNECTOR_NOT_FOUND}

    return {'result': db_service_code_master.CONNECTOR_FOUND, 'content': row[0]}
