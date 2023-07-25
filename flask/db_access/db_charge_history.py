# Universal imports
import copy
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods
import db_access.db_universal as db_universal

# Other db_access imports
import db_access.db_vehicle as db_vehicle
import db_access.db_charger as db_charger
import db_access.db_charge_current as db_charge_current

# Generics:
column_sql_translations = {'id': 'id', 'id_user_info': 'id_user_info', 'id_vehicle_info': 'id_vehicle_info', 'id_charger': 'id_charger',
                           'time_start': 'time_start', 'time_end': 'time_end', 'total_energy_drawn': 'total_energy_drawn',
                           'amount_payable': 'amount_payable', 'is_charge_finished': 'is_charge_finished'}
column_names_all = ['id', 'id_user_info', 'id_vehicle_info', 'id_charger', 'time_start',
                    'time_end', 'total_energy_drawn', 'amount_payable', 'is_charge_finished']
trailing_query = """
FROM charge_history
"""


def get_charge_history_hash_map(column_names=None, where_array=None):
    """
    | [SUPPORTING]
    | **Charge History Hashmap supported fields:** 
    | ['id', 'id_user_info', 'id_vehicle_info', 'id_charger', 'time_start',
    | 'time_end', 'total_energy_drawn', 'amount_payable', 'is_charge_finished']

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


def get_charge_history_dict(column_names=None, where_array=None):
    """
    | [SUPPORTING]
    | **Charge History Dictionary supported fields:** 
    | ['id', 'id_user_info', 'id_vehicle_info', 'id_charger', 'time_start',
    | 'time_end', 'total_energy_drawn', 'amount_payable', 'is_charge_finished']

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


def get_charge_history_active(id_user_info_sanitised):
    """
    | **[ENDPOINT]**
    | Attempts to retrieve a charge history entry based on user id. 
    | The entry is also joined with charge current, vehicle details, and charger details.
    | **Fields returned:** [{'id', 'time_start', 'total_energy_drawn', 'vehicle', 'charger'}]

    :param string id_user_info_sanitised: id_user_info_sanitised

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, CHARGE_HISTORY_NOT_FOUND, CHARGE_HISTORY_FOUND.
    :key 'content': (dictionary array, one/multiple) *('result' == CHARGE_HISTORY_FOUND)* Output.
    """

    # get charge history
    charge_history_dict_out = get_charge_history_dict(column_names=['id', 'id_vehicle_info',
                                                                    'id_charger', 'time_start', 'total_energy_drawn'],
                                                      where_array=[['id_user_info', id_user_info_sanitised], ['is_charge_finished', False]])
    # check if empty or error
    if charge_history_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.CHARGE_HISTORY_NOT_FOUND}
    if charge_history_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return charge_history_dict_out

    # get charge current using charge history id
    charge_current_dict_out = db_charge_current.get_charge_current_dict(column_names=['current_energy_drawn', 'rate_snapshot', 'last_updated'],
                                                                        where_array=[['id_charge_history', charge_history_dict_out['content'][0]['id']]])
    # check if empty or error
    # at this point, if empty returned, considered impossible under normal circumstances, internal error
    if charge_current_dict_out['result'] != db_service_code_master.SELECT_GENERIC_SUCCESS:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    # shove charge_current into charge_history
    key_values = charge_history_dict_out['content'][0]
    key_values.update(
        {'charge_current': charge_current_dict_out['content'][0]})
    # remove a key
    key_values.pop('id')

    # get all vehicles hash map
    vehicle_hash_map_out = db_vehicle.get_vehicle_hash_map(
        column_names=['name', 'model', 'vehicle_sn', 'connector_type'])
    # check if empty or error
    # at this point, if empty returned, considered impossible under normal circumstances, internal error
    if vehicle_hash_map_out['result'] != db_service_code_master.HASHMAP_GENERIC_SUCCESS:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    # get all chargers hash map
    charger_hash_map_out = db_charger.get_charger_hash_map(where_array=[['active', True]])
    # check if empty or error
    # at this point, if empty returned, considered impossible under normal circumstances, internal error
    if charger_hash_map_out['result'] != db_service_code_master.HASHMAP_GENERIC_SUCCESS:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    # replace id_vehicle_info with actual info
    db_helper_functions.update_dict_key(key_values, 'id_vehicle_info', 'vehicle',
                                        vehicle_hash_map_out['content'][key_values['id_vehicle_info']])
    # replace id_charger with actual info
    db_helper_functions.update_dict_key(
        key_values, 'id_charger', 'charger', charger_hash_map_out['content'][key_values['id_charger']])

    return {'result': db_service_code_master.CHARGE_HISTORY_FOUND,
            'content': key_values}


def get_charge_history_by_user_id(id_user_info_sanitised, filter_by):
    """
    | **[ENDPOINT]**
    | Retrieves a user's charge history.
    | **Fields returned:** 
    | 'in_progress': [{'id', 'time_start', 'total_energy_drawn', 'vehicle', 'charger'}]
    | 'complete': [{'id', 'time_start', 'time_end', 'total_energy_drawn', 'amount_payable', 'vehicle', 'charger'}]
    | 'all': [{'id', 'time_start', 'time_end', 'total_energy_drawn', 'amount_payable', 'is_charge_finished', 'vehicle', 'charger'}]

    :param string id_user_info_sanitised: id_user_info_sanitised
    :param string filter_by: 'in_progress', 'complete', 'all'

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, CHARGE_HISTORY_NOT_FOUND, CHARGE_HISTORY_FOUND, CONFIGURATION_ERROR. 
    :key 'content': (dictionary array) *('result' == CHARGE_HISTORY_FOUND)* Output.
    """

    # get charge history
    if filter_by == 'in_progress':
        charge_history_out = get_charge_history_dict(
            column_names=['id', 'id_vehicle_info', 'id_charger',
                          'time_start', 'total_energy_drawn'],
            where_array=[['id_user_info', id_user_info_sanitised], ['is_charge_finished', False]])
    elif filter_by == 'complete':
        charge_history_out = get_charge_history_dict(
            column_names=['id', 'id_vehicle_info', 'id_charger', 'time_start',
                          'time_end', 'total_energy_drawn', 'amount_payable'],
            where_array=[['id_user_info', id_user_info_sanitised], ['is_charge_finished', True]])
    elif filter_by == 'all':
        charge_history_out = get_charge_history_dict(
            column_names=['id', 'id_vehicle_info', 'id_charger', 'time_start', 'time_end',
                          'total_energy_drawn', 'amount_payable', 'is_charge_finished'],
            where_array=[['id_user_info', id_user_info_sanitised]])
    else:
        return {'result': db_service_code_master.CONFIGURATION_ERROR}

    # check if empty or error
    if charge_history_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.CHARGE_HISTORY_NOT_FOUND}
    if charge_history_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return charge_history_out

    # get vehicles hash map
    vehicle_hash_map_out = db_vehicle.get_vehicle_hash_map(
        column_names=['name', 'model', 'vehicle_sn', 'connector'])
    # check if empty or error (empty -> internal error)
    if vehicle_hash_map_out['result'] != db_service_code_master.HASHMAP_GENERIC_SUCCESS:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    # get chargers hash map
    charger_hash_map_out = db_charger.get_all_chargers_with_favourite_hash_map(id_user_info_sanitised)
    if charger_hash_map_out['result'] != db_service_code_master.CHARGER_FOUND:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    key_values = charge_history_out['content']


    # replace id_vehicle_info with actual info
    for row in key_values:
        db_helper_functions.update_dict_key(row, 'id_vehicle_info', 'vehicle',
                                            vehicle_hash_map_out['content'][row['id_vehicle_info']])
    # replace id_charger with actual info
    for row in key_values:
        db_helper_functions.update_dict_key(row, 'id_charger', 'charger',
                                            charger_hash_map_out['content'][row['id_charger']])

    return {'result': db_service_code_master.CHARGE_HISTORY_FOUND,
            'content': key_values}


def add_charge_history_initial(id_user_info_sanitised, id_vehicle_info_input, id_charger_input, id_charger_available_connector_input):
    """
    | **[ENDPOINT]**
    | Attempts to insert a charge history into the database.
    | This method will also add an entry to "charge current".

    :param string id_user_info_sanitised: id_user_info_sanitised
    :param string id_vehicle_info_input: id_vehicle_info_input
    :param string id_charger_input: id_charger_input
    :param string id_charger_available_connector_input: id_charger_available_connector_input

    :returns: Dictionary
    :key result: (one) INTERNAL_ERROR, CHARGE_HISTORY_CREATE_FAILURE, CHARGE_HISTORY_CREATE_SUCCESS.
    :key reason: (array, one/multiple) *('result' == CHARGE_HISTORY_CREATE_FAILURE)* ACCOUNT_NOT_FOUND, CHARGE_HISTORY_ALREADY_CHARGING, VEHICLE_NOT_FOUND, CHARGER_NOT_FOUND, CHARGE_HISTORY_INVALID_CHARGE_LEVEL
    """

    contains_errors = False
    error_list = []

    # 1: check that user is not already charging a vehicle
    charge_history_dict_out = get_charge_history_dict(column_names=['id'],
                                                      where_array=[['id_user_info', id_user_info_sanitised], ['is_charge_finished', False]])
    if charge_history_dict_out['result'] == db_service_code_master.SELECT_GENERIC_SUCCESS:
        contains_errors = True
        error_list.append(
            db_service_code_master.CHARGE_HISTORY_ALREADY_CHARGING)
    elif charge_history_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    # 2.1: check if vehicle exists
    vehicle_dict_out = db_vehicle.get_vehicle_dict(column_names=['id'],
                                                   where_array=[['id', id_vehicle_info_input]])
    if vehicle_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        contains_errors = True
        error_list.append(db_service_code_master.VEHICLE_NOT_FOUND)
    elif vehicle_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    # 2.2: store vehicle id (response contains sanitised id)
    else:
        id_vehicle_info_sanitised = vehicle_dict_out['content'][0]['id']

    # 3.1: check if charger exists
    charger_dict_out = db_charger.get_charger_dict(column_names=['id'],
                                                   where_array=[['id', id_charger_input], ['active', True]])
    if charger_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        contains_errors = True
        error_list.append(db_service_code_master.CHARGER_NOT_FOUND)
    elif charger_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    # 3.2: store charger id (response contains sanitised id)
    else:
        id_charger_sanitised = charger_dict_out['content'][0]['id']

    if contains_errors:
        return {'result': db_service_code_master.CHARGE_HISTORY_CREATE_FAILURE, 'reason': error_list}

    # 4: previous checks passed, generate rest of the fields
    id_charge_history = db_helper_functions.generate_uuid()
    time_start = db_helper_functions.generate_time_now()

    # 5: insert new charge history entry
    query = """
    INSERT INTO charge_history 
    (id, id_user_info, id_vehicle_info, id_charger, time_start, total_energy_drawn, is_charge_finished)
    VALUES (?,?,?,?,?,?,?) 
    """
    task = (id_charge_history, id_user_info_sanitised, id_vehicle_info_sanitised, id_charger_sanitised,
            time_start, 0, False)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    # 6: insert new charge current entry
    charge_current_response = db_charge_current.add_charge_current(
        id_charge_history, id_charger_sanitised, id_charger_available_connector_input)
    if charge_current_response['result'] != db_service_code_master.CHARGE_CURRENT_CREATE_SUCCESS:
        # destroy charge history entry
        # TODO
        return {'result': db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.CHARGE_HISTORY_CREATE_SUCCESS}


def finish_charge_history(id_user_info_sanitised):
    """
    | **[ENDPOINT]**
    | Attempts to close a charge history entry.
    | This method will also remove the corresponding "charge current" entry.

    :param string id_user_info_sanitised: id_user_info_sanitised

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, CHARGE_HISTORY_FINISH_FAILURE, CHARGE_HISTORY_FINISH_SUCCESS.
    :key 'reason': (array, one/multiple) *('result' == CHARGE_HISTORY_FINISH_FAILURE)* CHARGE_HISTORY_NOT_CHARGING
    """

    contains_errors = False
    error_list = []

    # 1: check if user is already charging a vehicle
    charge_history_dict_out = get_charge_history_dict(column_names=['id'],
                                                      where_array=[['id_user_info', id_user_info_sanitised], ['is_charge_finished', False]])
    if charge_history_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        contains_errors = True
        error_list.append(
            db_service_code_master.CHARGE_HISTORY_NOT_CHARGING)
    elif charge_history_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    else:
        id_charge_history_sanitised = charge_history_dict_out['content'][0]['id']

    if contains_errors:
        return {'result': db_service_code_master.CHARGE_HISTORY_FINISH_FAILURE,
                'reason': error_list}

    # 2: get charge current to determine price
    charge_current_dict_out = db_charge_current.get_charge_current_dict(column_names=['current_energy_drawn', 'rate_snapshot'],
                                                                        where_array=[['id_charge_history', id_charge_history_sanitised]])
    if charge_history_dict_out['result'] != db_service_code_master.SELECT_GENERIC_SUCCESS:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    print(charge_current_dict_out['content'][0])
    amount_payable = db_helper_functions.calculate_charge_cost(charge_current_dict_out['content'][0]['current_energy_drawn'],
                                                               charge_current_dict_out['content'][0]['rate_snapshot'])

    # 4: previous checks passed, generate rest of the fields
    time_end = db_helper_functions.generate_time_now()

    # 5: remove charge current entry
    charge_current_response = db_charge_current.remove_charge_current(
        id_charge_history_sanitised)
    if charge_current_response['result'] == db_service_code_master.INTERNAL_ERROR:
        return {'result': charge_current_response['result']}

    # 6: update charge history entry
    query = 'UPDATE charge_history SET total_energy_drawn=?, amount_payable=?, time_end=?, is_charge_finished=True WHERE id=?'
    task = (charge_current_dict_out['content'][0]['current_energy_drawn'], amount_payable,
            time_end, id_charge_history_sanitised)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.CHARGE_HISTORY_FINISH_SUCCESS}
