# Universal imports
import copy
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods
import db_access.db_universal as db_universal

# Other db_access imports
import db_access.db_connector_type as db_connector_type

# Generics:
column_sql_translations = {
    'id': 'id', 'id_charger': 'id_charger', 'id_connector_type': 'id_connector_type',
    'in_use': 'in_use', 'output_voltage': 'output_voltage', 'output_current': 'output_current'}
column_names_all = ['id', 'id_charger', 'id_connector_type',
                    'in_use', 'output_voltage', 'output_current']
trailing_query = """
FROM charger_available_connector
"""


def get_charger_available_connector_hash_map(column_names=None, where_array=None):
    """
    | [SUPPORTING]
    | **Charger Available Connector Hashmap supported fields:** 
    | ['id', 'id_charger', 'id_connector_type', 'in_use', 'output_voltage', 'output_current']

    :param array column_names: any combination of supported fields
    :param array where_array: containing more arrays[2-3], array[0] being WHERE column, array[1] being WHERE value, array[2] optionally being 'NOT' e.g. [['id', '0'], ['id', '1', 'NOT]]

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, HASHMAP_GENERIC_EMPTY, HASHMAP_GENERIC_SUCCESS. 
    :key 'content': (dictionary) *('result' == HASHMAP_GENERIC_SUCCESS)* Output. ('id' as key)
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    return db_universal.get_universal_hash_map(column_names=column_names,
                                               column_sql_translations=column_sql_translations,
                                               trailing_query=trailing_query,
                                               where_array=where_array)


def get_charger_available_connector_dict(column_names=None, where_array=None):
    """
    | [SUPPORTING]
    | **Charger Available Connector Dictionary supported fields:** 
    | ['id', 'id_charger', 'id_connector_type', 'in_use', 'output_voltage', 'output_current']

    :param array column_names: any combination of supported fields
    :param array where_array: containing more arrays[2-3], array[0] being WHERE column, array[1] being WHERE value, array[2] optionally being 'NOT' e.g. [['id', '0'], ['id', '1', 'NOT]]

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, SELECT_GENERIC_EMPTY, SELECT_GENERIC_SUCCESS. 
    :key 'content': (dictionary array) *('result' == SELECT_GENERIC_SUCCESS)* Output.
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    return db_universal.get_universal_dict(column_names=column_names,
                                           column_sql_translations=column_sql_translations,
                                           trailing_query=trailing_query,
                                           where_array=where_array)


def get_all_charger_connectors_decoded():
    """
    | **[INTERNAL]**
    | Gets a mapping of chargers' connectors.
    | **Fields returned:** {'id_charger':[{'id_charger_available_connector', 'in_use', 'connector_type':{...}}], 'id_charger':[{...}], ...}

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, AVAILABLE_CONNECTORS_NOT_FOUND, AVAILABLE_CONNECTORS_FOUND.
    :key 'content': (dictionary) *('result' == AVAILABLE_CONNECTORS_FOUND)* Output.
    """

    # get all chargers' available connectors
    charger_available_connector_dict_out = get_charger_available_connector_dict(column_names=['id', 'id_charger', 'in_use', 'id_connector_type'])
    # check if empty or error
    if charger_available_connector_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.AVAILABLE_CONNECTORS_NOT_FOUND}
    if charger_available_connector_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return charger_available_connector_dict_out

    # flatten charger_available_connector_out to dict with
    # {id_charger: [{id, in_use, id_connector_type}, ...], ...}
    charger_available_connector_dict = {}
    for row in charger_available_connector_dict_out['content']:
        if row['id_charger'] not in charger_available_connector_dict:
            charger_available_connector_dict.update({row['id_charger']: [{'id': row['id'], 'in_use': row['in_use'], 'id_connector_type': row['id_connector_type']}]})
        else:
            charger_available_connector_dict[row['id_charger']].append({'id': row['id'], 'in_use': row['in_use'], 'id_connector_type': row['id_connector_type']})

    # get all connector types
    connector_type_hash_out = db_connector_type.get_connector_type_hash_map()

    # update charger_available_connector_out id_connector_types to actual connector info
    for value in charger_available_connector_dict.values():
        for row in value:
            db_helper_functions.update_dict_key(dict=row, 
                                                key_to_update='id_connector_type', 
                                                key_new_name='connector_type',
                                                key_new_value=connector_type_hash_out['content'][row['id_connector_type']])

    return {'result': db_service_code_master.AVAILABLE_CONNECTORS_FOUND,
            'content': charger_available_connector_dict}


def set_charger_available_connector_in_use(id_charger_available_connector, set_to):
    """
    | **[INTERNAL]**
    | Sets a given id_charger_available_connector's 'in_use' state.

    :param string id_charger_available_connector: id_charger_available_connector
    :param boolean set_to: True or False

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, AVAILABLE_CONNECTOR_IN_USE or AVAILABLE_CONNECTOR_SET_USE_STATE_SUCCESS.
    """

    # sanitise input
    id_charger_available_connector_sanitised = db_helper_functions.string_sanitise(id_charger_available_connector)

    query = 'UPDATE charger_available_connector SET in_use=? WHERE id=?'
    task = (set_to, id_charger_available_connector_sanitised)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if transaction['rows_affected'] != 1:
        return {'result': db_service_code_master.AVAILABLE_CONNECTOR_IN_USE}

    return {'result': db_service_code_master.AVAILABLE_CONNECTOR_SET_USE_STATE_SUCCESS}


def update_charger_available_connector_electric_stats(id_charger_available_connector, output_voltage, output_current):
    pass
