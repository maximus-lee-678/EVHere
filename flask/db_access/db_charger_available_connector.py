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
    'id': 'id', 'id_charger': 'id_charger', 'id_connector_type': 'id_connector_type'}
column_names_all = ['id', 'id_charger', 'id_connector_type']
trailing_query = """
FROM charger_available_connector
"""


def get_charger_available_connector_hash_map(column_names=None, where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'id_charger', 'id_connector_type']\n
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


def get_charger_available_connector_dict(column_names=None, where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'id_charger', 'id_connector_type']\n
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


def get_all_charger_connectors_decoded():
    """
    Gets a mapping of chargers' connectors.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, AVAILABLE_CONNECTORS_NOT_FOUND or AVAILABLE_CONNECTORS_FOUND.\n
    <content> (if <result> is AVAILABLE_CONNECTORS_FOUND) {Dictionary} containing chargers' connectors.\n
    \t{"id_charger": {..connector info...}}
    """

    # get all chargers' available connectors
    charger_available_connector_dict_out = get_charger_available_connector_dict(
        column_names=['id_charger', 'id_connector_type'])
    # check if empty or error
    if charger_available_connector_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.AVAILABLE_CONNECTORS_NOT_FOUND}
    if charger_available_connector_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return charger_available_connector_dict_out

    # flatten charger_available_connector_out to dict with
    # key: id_charger
    # value: [id_connector_type]
    charger_available_connector_dict = {}
    for row in charger_available_connector_dict_out['content']:
        if row['id_charger'] not in charger_available_connector_dict:
            charger_available_connector_dict.update(
                {row['id_charger']: [row['id_connector_type']]})
        else:
            charger_available_connector_dict[row['id_charger']].append(
                row['id_connector_type'])

    # get all connector types
    connector_type_hash_out = db_connector_type.get_connector_type_hash_map()

    # update charger_available_connector_out id_connector_types to actual connector info
    # original content: {[id, ...], [id, ...], ...}
    # cycle through each array and each index of array
    # update each array index to contain matched id_connector_type to connector_type_out dict
    # final content: {[{connector_info}, ...], [{connector_info}, ...], ...}
    for value in charger_available_connector_dict.values():
        for index, id_connector_type in enumerate(value):
            value[index] = connector_type_hash_out['content'][id_connector_type]

    return {'result': db_service_code_master.AVAILABLE_CONNECTORS_FOUND,
            'content': charger_available_connector_dict}
