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
                           'address': 'address', 'currently_open': 'currently_open', 'pv_current_in': 'pv_current_in', 'pv_energy_level': 'pv_energy_level',
                           'rate_current': 'rate_current', 'rate_predicted': 'rate_predicted', 'active': 'active', 'last_updated': 'last_updated'}
column_names_all = ['id', 'name', 'latitude', 'longitude', 'address', 'currently_open', 'pv_current_in', 'pv_energy_level',
                    'rate_current', 'rate_predicted', 'active', 'last_updated', 'available_connector']
trailing_query = """
FROM charger
"""


def get_charger_hash_map(column_names=None, where_array=None):
    """
    | **[SUPPORTING]**
    | **Charger Hashmap supported fields:** 
    | ['id', 'name', 'latitude', 'longitude', 'address', 'currently_open', 
    | 'pv_current_in', 'pv_energy_level', 'rate_current', 'rate_predicted', 'active', 'last_updated', 'available_connector']

    :param array column_names: any combination of supported fields
    :param array where_array: containing more arrays[2-3], array[0] being WHERE column, array[1] being WHERE value, array[2] optionally being 'NOT' e.g. [['id', '0'], ['id', '1', 'NOT]]

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, HASHMAP_GENERIC_EMPTY, HASHMAP_GENERIC_SUCCESS. 
    :key 'content': (dictionary) *('result' == HASHMAP_GENERIC_SUCCESS)* Output. ('id' as key)
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    get_connectors = False
    has_temp_id = False
    if 'available_connector' in column_names:
        get_connectors = True
        column_names.remove('available_connector')
        if 'id' not in column_names:
            has_temp_id = True
            column_names.append('id')

    charger_hash_out = db_universal.get_universal_hash_map(column_names=column_names,
                                                           column_sql_translations=column_sql_translations,
                                                           trailing_query=trailing_query,
                                                           where_array=where_array)

    if charger_hash_out['result'] == db_service_code_master.HASHMAP_GENERIC_EMPTY:
        return charger_hash_out

    if not get_connectors:
        return charger_hash_out

    charger_available_connector_dict_out = db_charger_available_connector.get_all_charger_connectors_decoded()

    # append to original dict
    if not has_temp_id:
        for key, value in charger_hash_out['content'].items():
            db_helper_functions.update_dict_key(
                dict=value, key_to_update='available_connector', new_key_name=None, new_key_value=charger_available_connector_dict_out['content'][key])
    else:
        for key, value in charger_hash_out['content'].items():
            db_helper_functions.update_dict_key(
                dict=value, key_to_update='available_connector', new_key_name=None, new_key_value=charger_available_connector_dict_out['content'][key])
            value.pop('id')

    return charger_hash_out


def get_charger_dict(column_names=None, where_array=None):
    """
    | **[SUPPORTING]**
    | **Charger Dictionary supported fields:** 
    | ['id', 'name', 'latitude', 'longitude', 'address', 'currently_open', 
    | 'pv_current_in', 'pv_energy_level', 'rate_current', 'rate_predicted', 'active', 'last_updated', 'available_connector']

    :param array column_names: any combination of supported fields
    :param array where_array: containing more arrays[2-3], array[0] being WHERE column, array[1] being WHERE value, array[2] optionally being 'NOT' e.g. [['id', '0'], ['id', '1', 'NOT]]

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, SELECT_GENERIC_EMPTY, SELECT_GENERIC_SUCCESS. 
    :key 'content': (dictionary array) *('result' == SELECT_GENERIC_SUCCESS)* Output.
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    get_connectors = False
    has_temp_id = False
    if 'available_connector' in column_names:
        get_connectors = True
        column_names.remove('available_connector')
        if 'id' not in column_names:
            has_temp_id = True
            column_names.append('id')

    charger_dict_out = db_universal.get_universal_dict(column_names=column_names,
                                                       column_sql_translations=column_sql_translations,
                                                       trailing_query=trailing_query,
                                                       where_array=where_array)

    if charger_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return charger_dict_out

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
                dict=row, key_to_update='available_connector', new_key_name=None, new_key_value=charger_available_connector_dict_out['content'][row['id']])
    else:
        for row in charger_dict_out['content']:
            db_helper_functions.update_dict_key(
                dict=row, key_to_update='available_connector', new_key_name=None, new_key_value=charger_available_connector_dict_out['content'][row['id']])
            row.pop('id')

    return charger_dict_out


def get_all_chargers_with_favourite_dict(id_user_info_sanitised):
    """
    | **[ENDPOINT/INTERNAL]**
    | Retrieves ALL chargers from database. Also includes 'is_favourite'. (Dictionary)
    | **Fields returned:** [{'id', 'name', 'latitude', 'longitude', 'address', 'currently_open', 'pv_current_in', 
    | 'pv_energy_level', 'rate_current', 'rate_predicted', 'active', 'last_updated', 'available_connector', 'is_favourite'}]

    :param string id_user_info_sanitised: id_user_info_sanitised

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, CHARGER_NOT_FOUND, CHARGER_FOUND. 
    :key 'content': (dictionary array) *('result' == CHARGER_FOUND)* Output.
    """

    # get charger hash map
    charger_dict_out = get_charger_dict(where_array=[['active', True]])
    # check if empty or error
    if charger_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.CHARGER_NOT_FOUND}
    if charger_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return charger_dict_out

    key_values = charger_dict_out['content']

    add_favourites(key_values, id_user_info_sanitised)

    return {'result': db_service_code_master.CHARGER_FOUND,
            'content': key_values}


def get_all_chargers_with_favourite_hash_map(id_user_info_sanitised):
    """
    | **[INTERNAL]**
    | Retrieves ALL chargers from database. Also includes 'is_favourite'. (Hashmap)
    | **Fields returned:** {'id', 'name', 'latitude', 'longitude', 'address', 'currently_open', 'pv_current_in', 
    | 'pv_energy_level', 'rate_current', 'rate_predicted', 'active', 'last_updated', 'available_connector', 'is_favourite'}

    :param string id_user_info_sanitised: id_user_info_sanitised

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, CHARGER_NOT_FOUND, CHARGER_FOUND. 
    :key 'content': (dictionary) *('result' == CHARGER_FOUND)* Output.
    """

    # get charger hash map
    charger_dict_out = get_charger_hash_map(where_array=[['active', True]])
    # check if empty or error
    if charger_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.CHARGER_NOT_FOUND}
    if charger_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return charger_dict_out

    content_dict = charger_dict_out['content']
    
    add_favourites(content_dict, id_user_info_sanitised)

    return {'result': db_service_code_master.CHARGER_FOUND,
            'content': content_dict}


def add_favourites(charger_dict_or_hash, id_user_info_sanitised):
    """
    | **[INTERNAL]**
    | Adds user charger favourites to a dictionary array or hashmap.
    | No return as dicts and arrays are pass by reference.

    :param string charger_dict_or_hash: charger dictionary or hashmap
    :param string id_user_info_sanitised: id_user_info_sanitised
    """

    # get favourite chargers
    favourites_array_out = db_favourite_charger.get_user_favourite_charger_id_array(
        id_user_info_sanitised)
    # check if error
    if favourites_array_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return favourites_array_out
    
    # check if empty, return dict with additional key is_favourite all set to false
    # else return with additional key is_favourite based on key appearance in favourites_array_out
    if type(charger_dict_or_hash) is list:
        if favourites_array_out['result'] == db_service_code_master.FAVOURITE_CHARGERS_NOT_FOUND:
            for row in charger_dict_or_hash:
                db_helper_functions.update_dict_key(
                    row, None, 'is_favourite', False)
        else:
            for row in charger_dict_or_hash:
                db_helper_functions.update_dict_key(
                    row, None, 'is_favourite', True if row['id'] in favourites_array_out['content'] else False)
    elif type(charger_dict_or_hash) is dict:
        if favourites_array_out['result'] == db_service_code_master.FAVOURITE_CHARGERS_NOT_FOUND:
            for value in charger_dict_or_hash.values():
                db_helper_functions.update_dict_key(
                    value, None, 'is_favourite', False)
        else:
            for value in charger_dict_or_hash.values():
                db_helper_functions.update_dict_key(
                    value, None, 'is_favourite', True if value['id'] in favourites_array_out['content'] else False)