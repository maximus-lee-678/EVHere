# Universal imports
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods

# Other db_access imports
# 


def get_all_charger_available_connector():
    """
    Retrieves ALL chargers' connectors from database.\n
    Returns Dictionary with keys:\n
    <result> AVAILABLE_CONNECTOR_NOT_FOUND or AVAILABLE_CONNECTORS_FOUND.\n
    <content> (if <result> is AVAILABLE_CONNECTORS_FOUND) [{Dictionary Array}] containing chargers' available connector(s) information.\n
    \t"keys":\n
    \t{"id_charger", "id_connector_type"}
    """

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id_charger, id_connector_type FROM charger_available_connector')

    rows = cursor.fetchall()
    db_methods.close_connection(conn)

    if db_methods.check_fetchall_has_nothing(rows):
        return {'result': db_service_code_master.AVAILABLE_CONNECTOR_NOT_FOUND}

    key_values = []
    # transforming array to key-values
    for row in rows:
        key_values.append({"id_charger": row[0], "id_connector_type": row[1]})

    return {'result': db_service_code_master.AVAILABLE_CONNECTORS_FOUND, 'content': key_values}
