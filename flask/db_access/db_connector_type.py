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
    <result> INTERNAL_ERROR, CONNECTOR_NOT_FOUND or CONNECTOR_FOUND.\n
    <content> (if <result> is CONNECTOR_FOUND) [{Dictionary Array}] containing connector information.\n
    \t"keys":\n
    \t{"id", "name_short", "name_long", "name_connector"}
    """

    query = 'SELECT id, name_short, name_long, name_connector FROM connector_type'

    select = db_methods.safe_select(query=query, task=None, get_type='all')

    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.CONNECTOR_NOT_FOUND}

    key_values = []
    # transforming array to key-values
    for row in select['content']:
        key_values.append(
            {"id": row[0], "name_short": row[1], "name_long": row[2], "name_connector": row[3]})

    return {'result': db_service_code_master.CONNECTOR_FOUND, 'content': key_values}


def get_connector_id_by_name_short(name_short_input):
    """
    Retrieves a single connector's id based on name from database.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CONNECTOR_NOT_FOUND or CONNECTOR_FOUND.\n
    <content> (if <result> is CONNECTOR_FOUND) =Value= containing connector ID.
    """

    # sanitise name_short
    name_short_sanitised = db_helper_functions.string_sanitise(
        name_short_input)

    query = 'SELECT id FROM connector_type WHERE name_short=?'
    task = (name_short_sanitised,)

    select = db_methods.safe_select(query=query, task=task, get_type='one')

    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.CONNECTOR_NOT_FOUND}

    return {'result': db_service_code_master.CONNECTOR_FOUND, 'content': select['content'][0]}
