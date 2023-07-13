# Universal imports
import copy
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods
import db_access.db_universal as db_universal

# Other db_access imports
import db_access.db_favourite_charger as db_favourite_charger
import db_access.db_charger_available_connector as db_charger_available_connector

# Generics:
column_sql_translations = {'id': 'id', 'name': 'name', 'latitude': 'latitude', 'longitude': 'longitude',
                           'address': 'address', 'provider': 'provider', 'connectors': 'connectors', 'online': 'c.online',
                           'kilowatts': 'kilowatts', 'twenty_four_hours': 'twenty_four_hours', 'last_updated': 'last_updated'}
column_names_all = ['id', 'name', 'latitude', 'longitude', 'address', 'provider',
                    'connectors', 'online', 'kilowatts', 'twenty_four_hours', 'last_updated', 'connector_info']
trailing_query = """
FROM charger AS c
"""


def get_charger_hash_map(column_names=None, where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'name', 'latitude', 'longitude', 'address', 'provider',
                    'connectors', 'online', 'kilowatts', 'twenty_four_hours', 'last_updated', 'connector_info']\n
    \twhere_array >> an [Array] containing more [Arrays][2], [Array][0] being WHERE column and [Array][1] being WHERE value e.g. [['id', '0'], ['id', '1']\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, HASHMAP_GENERIC_EMPTY or HASHMAP_GENERIC_SUCCESS.\n
    <content> (if <result> is HASHMAP_GENERIC_SUCCESS) {Dictionary} containing table information.\n
    \t{"id": {...key-values...}}
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    get_connectors = False
    has_temp_id = False
    if 'connector_info' in column_names:
        get_connectors = True
        column_names.remove('connector_info')
        if 'id' not in column_names:
            has_temp_id = True
            column_names.append('id')


    charger_hash_out = db_universal.get_universal_hash_map(column_names=column_names,
                                                           column_sql_translations=column_sql_translations,
                                                           trailing_query=trailing_query,
                                                           where_array=where_array)

    if not get_connectors:
        return charger_hash_out

    charger_available_connector_dict_out = db_charger_available_connector.get_all_charger_connectors_decoded()
    
    # append to original dict
    if not has_temp_id:
        for key, value in charger_hash_out['content'].items():
            db_helper_functions.update_dict_key(
                dict=value, key_to_update='connector_info', new_key_name=None, new_key_value=charger_available_connector_dict_out['content'][key])
    else:
        for key, value in charger_hash_out['content'].items():
            db_helper_functions.update_dict_key(
                dict=value, key_to_update='connector_info', new_key_name=None, new_key_value=charger_available_connector_dict_out['content'][key])
            value.pop('id')
    
    return charger_hash_out


def get_charger_dict(column_names=None, where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'name', 'latitude', 'longitude', 'address', 'provider',
                    'connectors', 'online', 'kilowatts', 'twenty_four_hours', 'last_updated', 'connector_info']\n
    \twhere_array >> an [Array] containing more [Arrays][2], [Array][0] being WHERE column and [Array][1] being WHERE value e.g. [['id', '0'], ['id', '1']\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, SELECT_GENERIC_EMPTY or SELECT_GENERIC_SUCCESS.\n
    <content> (if <result> is SELECT_GENERIC_SUCCESS) {Dictionary} containing table information.\n
    \t{{...key-values...}}
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    get_connectors = False
    has_temp_id = False
    if 'connector_info' in column_names:
        get_connectors = True
        column_names.remove('connector_info')
        if 'id' not in column_names:
            has_temp_id = True
            column_names.append('id')

    charger_dict_out = db_universal.get_universal_dict(column_names=column_names,
                                                       column_sql_translations=column_sql_translations,
                                                       trailing_query=trailing_query,
                                                       where_array=where_array)

    if not get_connectors:
        return charger_dict_out

    charger_available_connector_dict_out = db_charger_available_connector.get_all_charger_connectors_decoded()
    
    # check if empty or error (empty -> error)
    if charger_available_connector_dict_out['result'] == db_service_code_master.AVAILABLE_CONNECTORS_NOT_FOUND:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if charger_available_connector_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return charger_available_connector_dict_out

    # append to original dict
    if not has_temp_id:
        for row in charger_dict_out['content']:
            db_helper_functions.update_dict_key(
                dict=row, key_to_update='connector_info', new_key_name=None, new_key_value=charger_available_connector_dict_out['content'][row['id']])
    else:
        for row in charger_dict_out['content']:
            db_helper_functions.update_dict_key(
                dict=row, key_to_update='connector_info', new_key_name=None, new_key_value=charger_available_connector_dict_out['content'][row['id']])
            row.pop('id')

    return charger_dict_out


def get_all_chargers(id_user_info_sanitised):
    """
    Retrieves ALL chargers from database. If user id is specified, adds an additional column indicating if charger is favourited.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CHARGER_NOT_FOUND or CHARGER_FOUND.\n
    <type> (if <result> is CHARGER_FOUND) CHARGER_WITH_FAVOURITE or CHARGER_WITHOUT_FAVOURITE.\n
    <content> (if <result> is CHARGER_FOUND) [{Dictionary Array}] containing charger information.\n
    \t"keys":\n
    \t{"id", "name", "latitude", "longitude", "address", "provider", "connectors", 
    "online", "kilowatts", "twenty_four_hours", "last_updated", "is_favourite", "connector_info"}
    """

    # get charger hash map
    charger_dict_out = get_charger_dict(column_names=['id', 'name', 'latitude', 'longitude', 'address', 'provider',
                                                          'connectors', 'online', 'kilowatts', 'twenty_four_hours', 'last_updated', 'connector_info'])
    # check if empty or error
    if charger_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.CHARGER_NOT_FOUND}
    if charger_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return charger_dict_out

    key_values = charger_dict_out['content']

    if id_user_info_sanitised is None:
        return {'result': db_service_code_master.CHARGER_FOUND,
                'type': db_service_code_master.CHARGER_WITHOUT_FAVOURITE,
                'content': key_values}

    # get favourite chargers
    favourites_array_out = db_favourite_charger.get_user_favourite_charger_ids(
        id_user_info_sanitised)
    # check if error
    if favourites_array_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return favourites_array_out
    # check if empty, return dict with additional key is_favourite all set to false
    if favourites_array_out['result'] == db_service_code_master.FAVOURITE_CHARGERS_NOT_FOUND:
        for row in key_values:
            db_helper_functions.update_dict_key(
                row, None, 'is_favourite', False)
    # user has favourites, return dict with additional key is_favourite based on key appearance in favourites_array_out
    else:
        for row in key_values:
            db_helper_functions.update_dict_key(
                row, None, 'is_favourite', True if row['id'] in favourites_array_out['content'] else False)

    return {'result': db_service_code_master.CHARGER_FOUND,
            'type': db_service_code_master.CHARGER_WITH_FAVOURITE,
            'content': key_values}
