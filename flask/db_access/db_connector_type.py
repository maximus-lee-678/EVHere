# Universal imports
import copy
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods
import db_access.db_universal as db_universal

# Other db_access imports
#

# Generics:
column_sql_translations = {'id': 'id', 'name_short': 'name_short',
                           'name_long': 'name_long', 'name_connector': 'name_connector'}
column_names_all = ['id', 'name_short', 'name_long', 'name_connector']
trailing_query = """
FROM connector_type
"""


def get_connector_type_hash_map(column_names=None,where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'name_short', 'name_long', 'name_connector']\n
    \twhere_array >> an [Array] containing more [Arrays][2], [Array][0] being WHERE column and [Array][1] being WHERE value e.g. [['id', '0'], ['id', '1']\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, HASHMAP_GENERIC_EMPTY or HASHMAP_GENERIC_SUCCESS.\n
    <content> (if <result> is HASHMAP_GENERIC_SUCCESS) {Dictionary} containing table information.\n
    \t{"id": {...key-values...}}
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    return db_universal.get_universal_hash_map(column_names=column_names,
                                               column_sql_translations=column_sql_translations,
                                               trailing_query=trailing_query,
                                               where_array=where_array)


def get_connector_type_dict(column_names=None,where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'name_short', 'name_long', 'name_connector']\n
    \twhere_array >> an [Array] containing more [Arrays][2], [Array][0] being WHERE column and [Array][1] being WHERE value e.g. [['id', '0'], ['id', '1']\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, SELECT_GENERIC_EMPTY or SELECT_GENERIC_SUCCESS.\n
    <content> (if <result> is SELECT_GENERIC_SUCCESS) {Dictionary} containing table information.\n
    \t{{...key-values...}}
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    return db_universal.get_universal_dict(column_names=column_names,
                                           column_sql_translations=column_sql_translations,
                                           trailing_query=trailing_query,
                                           where_array=where_array)


def get_all_connectors():
    """
    Retrieves ALL connectors from database.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CONNECTOR_NOT_FOUND or CONNECTOR_FOUND.\n
    <content> (if <result> is CONNECTOR_FOUND) [{Dictionary Array}] containing connector information.\n
    \t"keys":\n
    \t{"id", "name_short", "name_long", "name_connector"}
    """

    connector_type_dict_out = get_connector_type_dict()
    # check if empty or error
    if connector_type_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.CONNECTOR_NOT_FOUND}
    if connector_type_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return connector_type_dict_out

    return {'result': db_service_code_master.CONNECTOR_FOUND, 'content': connector_type_dict_out['content']}
