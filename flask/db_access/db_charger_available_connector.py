import db_access.db_helper_functions as db_helper_functions
import db_access.db_methods as db_methods

CONNECTOR_FOUND = 100
CONNECTOR_NOT_FOUND = 101

service_code_dict = {
    CONNECTOR_FOUND: "Found connectors.",
    CONNECTOR_NOT_FOUND: "No connectors found."
}

def get_all_charger_available_connector():
    """
    Retrieves ALL chargers' connectors from database.\n
    Returns Dictionary with keys:\n
    <result> CONNECTOR_NOT_FOUND or CONNECTOR_FOUND.\n
    <content> (if <result> is CONNECTOR_FOUND) Dictionary containing chargers' available connector(s) information.
    """
    
    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id_charger, id_connector_type FROM charger_available_connector')

    rows = cursor.fetchall()
    db_methods.close_connection(conn)

    if db_methods.check_fetchall_has_nothing(rows):
        return {'result': CONNECTOR_NOT_FOUND}
    
    key_values = []
    # transforming array to key-values
    for row in rows:
        key_values.append({"id_charger": row[0], "id_connector_type": row[1]})

    return {'result': CONNECTOR_FOUND, 'content': key_values}
