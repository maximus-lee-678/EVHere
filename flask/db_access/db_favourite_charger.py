# Universal imports
import copy
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods
import db_access.db_universal as db_universal

# Other db_access imports
import db_access.db_charger as db_charger

# Generics:
column_sql_translations = {'id': 'id', 'id_user_info': 'id_user_info', 'id_charger': 'id_charger'}
column_names_all = ['id', 'id_user_info', 'id_charger']
trailing_query = """
FROM favourited_chargers
"""


def get_favourite_charger_hash_map(column_names=None, where_array=None):
    """
    | **[SUPPORTING]**
    | **Favourite Charger Hashmap supported fields:** 
    | ['id', 'id_user_info', 'id_charger']

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


def get_favourite_charger_dict(column_names=None, where_array=None):
    """
    | **[SUPPORTING]**
    | **Favourite Charger Dictionary supported fields:** 
    | ['id', 'id_user_info', 'id_charger']

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


def get_user_favourite_chargers(id_user_info_sanitised):
    """
    | **[ENDPOINT]**
    | Get a user's favourite chargers.
    | **Fields returned:** 
    | [{'id', 'name', 'latitude', 'longitude', 'address', 'currently_open', 'pv_voltage_in', 'pv_current_in', 'pv_voltage_out', 'pv_current_out',
    | 'rate_current', 'rate_predicted', 'active', 'last_updated', 'available_connector'}]

    :param string id_user_info_sanitised: id_user_info_sanitised

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, FAVOURITE_CHARGERS_NOT_FOUND, FAVOURITE_CHARGERS_FOUND.
    :key 'content': (dictionary array) *('result' == FAVOURITE_CHARGERS_FOUND)* Output.
    """

    # get favourite chargers
    favourites_array_out = get_user_favourite_charger_id_array(id_user_info_sanitised=id_user_info_sanitised)
    # check if error or empty
    if favourites_array_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return favourites_array_out
    if favourites_array_out['result'] == db_service_code_master.FAVOURITE_CHARGERS_NOT_FOUND:
        return favourites_array_out

    # get all chargers
    charger_hash_map_out = db_charger.get_charger_hash_map(where_array=[['active', True]])
    # check if empty or error (empty -> internal error)
    if charger_hash_map_out['result'] != db_service_code_master.HASHMAP_GENERIC_SUCCESS:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    # map array of ids to dict array
    favourite_charger_details_array = [charger_hash_map_out['content'][item]
                                       for item in favourites_array_out['content']]

    return {'result': db_service_code_master.FAVOURITE_CHARGERS_FOUND,
            'content': favourite_charger_details_array}


def add_favourite_charger(id_user_info_sanitised, id_charger_input):
    """
    | **[ENDPOINT]**
    | Attempts to add a favourite charger entry to the database.

    :param string id_user_info_sanitised: id_user_info_sanitised
    :param string id_charger_input: id_charger_input

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, FAVOURITE_CHARGER_MODIFY_SUCCESS, FAVOURITE_CHARGER_MODIFY_FAILURE.
    :key 'reason': (array, one/multiple) *('result' == FAVOURITE_CHARGER_MODIFY_FAILURE)* CHARGER_NOT_FOUND, FAVOURITE_CHARGER_DUPLICATE_ENTRY.
    """

    contains_errors = False
    error_list = []

    # 1.1: check if charger exists
    charger_dict_out = db_charger.get_charger_dict(column_names=['id'],
                                                   where_array=[['id', id_charger_input], ['active', True]])
    if charger_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        contains_errors = True
        error_list.append(db_service_code_master.CHARGER_NOT_FOUND)
    elif charger_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        contains_errors = True
        error_list.append(charger_dict_out['result'])
    # 1.2: store charger id (response contains sanitised id)
    else:
        id_charger_sanitised = charger_dict_out['content'][0]['id']

    # 2.1: ensure charger not already favourited (no dupes)
    favourite_charger_dict_out = get_favourite_charger_dict(column_names=['id'],
                                                            where_array=[['id_user_info', id_user_info_sanitised], ['id_charger', id_charger_sanitised]])
    if favourite_charger_dict_out['result'] == db_service_code_master.SELECT_GENERIC_SUCCESS:
        contains_errors = True
        error_list.append(db_service_code_master.FAVOURITE_CHARGER_DUPLICATE_ENTRY)
    if favourite_charger_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        contains_errors = True
        error_list.append(favourite_charger_dict_out['result'])

    if contains_errors:
        return {'result': db_service_code_master.FAVOURITE_CHARGER_MODIFY_FAILURE, 
                'reason': error_list}

    id = db_helper_functions.generate_uuid()

    query = 'INSERT INTO favourited_chargers VALUES (?,?,?)'
    task = (id, id_user_info_sanitised, id_charger_sanitised)

    # 3: add entry
    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.FAVOURITE_CHARGER_MODIFY_SUCCESS}


def remove_favourite_charger(id_user_info_sanitised, id_charger_input):
    """
    | **[ENDPOINT]**
    | Attempts to remove a favourite charger entry from the database.

    :param string id_user_info_sanitised: id_user_info_sanitised
    :param string id_charger_input: id_charger_input

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, FAVOURITE_CHARGER_MODIFY_SUCCESS, FAVOURITE_CHARGER_MODIFY_FAILURE.
    :key 'reason': (array, one) *('result' == FAVOURITE_CHARGER_MODIFY_FAILURE)* FAVOURITE_CHARGERS_NOT_FOUND.
    """

    id_charger_sanitised = db_helper_functions.string_sanitise(id_charger_input)

    query = 'DELETE FROM favourited_chargers WHERE id_user_info=? AND id_charger=?'
    task = (id_user_info_sanitised, id_charger_sanitised)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if transaction['rows_affected'] != 1:
        return {'result': db_service_code_master.FAVOURITE_CHARGER_MODIFY_FAILURE, 
                'reason': [db_service_code_master.FAVOURITE_CHARGERS_NOT_FOUND]}

    return {'result': db_service_code_master.FAVOURITE_CHARGER_MODIFY_SUCCESS}


def get_user_favourite_charger_id_array(id_user_info_sanitised):
    """
    | **[INTERNAL]**
    | Get an array of a user's favourite charger ids.

    :param string id_user_info_sanitised: id_user_info_sanitised

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, FAVOURITE_CHARGERS_NOT_FOUND, FAVOURITE_CHARGERS_FOUND.
    :key 'content': (array) *('result' == FAVOURITE_CHARGERS_FOUND)* Output.
    """

    favourite_charger_dict_out = get_favourite_charger_dict(column_names=['id_charger'],
                                                            where_array=[['id_user_info', id_user_info_sanitised]])
    # check if error
    if favourite_charger_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return favourite_charger_dict_out
    # check if empty
    if favourite_charger_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.FAVOURITE_CHARGERS_NOT_FOUND}

    # flatten dict
    favourites_array = [row['id_charger']
                        for row in favourite_charger_dict_out['content']]

    return {'result': db_service_code_master.FAVOURITE_CHARGERS_FOUND, 'content': favourites_array}
