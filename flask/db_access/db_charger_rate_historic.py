# Universal imports
import copy
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods
import db_access.db_universal as db_universal

# Other db_access imports
#

# Generics:
column_sql_translations = {
    'id': 'id', 'id_charger': 'id_charger', 'rate': 'rate', 'timestamp': 'timestamp'}
column_names_all = ['id', 'id_charger', 'rate', 'timestamp']
trailing_query = """
FROM charger_rate_historic
"""


def get_charger_rate_historic_hash_map(column_names=None, where_array=None):
    """
    | [SUPPORTING]
    | **Charger Rate Historic Hashmap supported fields:** 
    | ['id', 'id_charger', 'rate', 'timestamp']

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


def get_charger_rate_historic_dict(column_names=None, where_array=None):
    """
    | [SUPPORTING]
    | **Charger Rate Historic Dictionary supported fields:** 
    | ['id', 'id_charger', 'rate', 'timestamp']

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

def get_all_past_charger_rates(id_charger):
    """
    | **[ENDPOINT]**
    | Retrieves ALL charger ids from database. (Dictionary)
    | **Fields returned:** [{'id'}]

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, CHARGER_RATE_HISTORIC_NOT_FOUND, CHARGER_RATE_HISTORIC_FOUND. 
    :key 'content': (dictionary array) *('result' == CHARGER_RATE_HISTORIC_FOUND)* Output.
    """
    
    charger_rate_historic_out = get_charger_rate_historic_dict(where_array=[['id_charger', id_charger]])
    if charger_rate_historic_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.CHARGER_RATE_HISTORIC_NOT_FOUND}
    if charger_rate_historic_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return charger_rate_historic_out
    
    key_values = charger_rate_historic_out['content']

    return {'result': db_service_code_master.CHARGER_RATE_HISTORIC_FOUND,
            'content': key_values}