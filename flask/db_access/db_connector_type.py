# Universal imports
import copy
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods
import db_access.db_universal as db_universal

# Other db_access imports
#

# Generics:
column_sql_translations = {'id': 'id', 'current_type': 'current_type', 'name_connector': 'name_connector',
                           'output_voltage_max': 'output_voltage_max', 'output_current_max': 'output_current_max'}
column_names_all = ['id', 'current_type', 'name_connector', 'output_voltage_max', 'output_current_max']
trailing_query = """
FROM connector_type
"""


def get_connector_type_hash_map(column_names=None,where_array=None):
    """
    | **[SUPPORTING]**
    | **Connector Type Hashmap supported fields:** 
    | ['id', 'current_type', 'name_connector', 'output_voltage_max', 'output_current_max']

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


def get_connector_type_dict(column_names=None,where_array=None):
    """
    | **[SUPPORTING]**
    | **Connector Type Dictionary supported fields:** 
    | ['id', 'current_type', 'name_connector', 'output_voltage_max', 'output_current_max']

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


def get_all_connectors():
    """
    | **[ENDPOINT]**
    | Retrieves ALL connector types from database.
    | **Fields returned:** [{'id', 'name_short', 'name_long', 'name_connector'}]

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, CONNECTOR_NOT_FOUND, CONNECTOR_FOUND. 
    :key 'content': (dictionary array) *('result' == CONNECTOR_FOUND)* Output.
    """

    connector_type_dict_out = get_connector_type_dict()
    # check if empty or error
    if connector_type_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.CONNECTOR_NOT_FOUND}
    if connector_type_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return connector_type_dict_out

    return {'result': db_service_code_master.CONNECTOR_FOUND, 'content': connector_type_dict_out['content']}
