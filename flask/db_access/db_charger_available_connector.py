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

    query = 'SELECT id_charger, id_connector_type FROM charger_available_connector'

    select = db_methods.safe_select(query=query, task=None, get_type='all')
    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.AVAILABLE_CONNECTOR_NOT_FOUND}

    # transforming array to key-values
    key_values = [{"id_charger": row[0], "id_connector_type": row[1]} 
                  for row in select['content']]
    

    return {'result': db_service_code_master.AVAILABLE_CONNECTORS_FOUND, 'content': key_values}
