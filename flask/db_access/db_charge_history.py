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
    \tcolumn_names >> any combination of ['id', 'id_user_info', 'id_vehicle_info', 'id_charger', 'time_start',
                    'time_end', 'total_energy_drawn', 'amount_payable', 'is_charge_finished']\n
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


def get_charge_history_dict(column_names=None, where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'id_user_info', 'id_vehicle_info', 'id_charger', 'time_start',
                    'time_end', 'total_energy_drawn', 'amount_payable', 'is_charge_finished']\n
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


def get_charge_history_active(id_user_info_sanitised):
    """
    Attempts to retrieve a charge history entry based on user id. 
    The entry is also joined with charge current, vehicle details, and charger details.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CHARGE_HISTORY_NOT_FOUND or CHARGE_HISTORY_FOUND.\n
    <content> (if <result> is CHARGE_HISTORY_FOUND) {Dictionary} containing charge history information.
    \t{"time_start", "percentage_current", "charge_current", "vehicle", "charger"}
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
    charger_hash_map_out = db_charger.get_charger_hash_map(column_names=['name', 'latitude', 'longitude', 'address', 'currently_open',
                                                                         'pv_current_in', 'pv_energy_level', 'rate_current', 'rate_predicted',
                                                                         'active', 'last_updated', 'available_connector'],
                                                           where_array=[['active', True]])
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
    Retrieve's a user's charge history.
    \tfilter_by >> in_progress, complete, all\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CHARGE_HISTORY_NOT_FOUND, CHARGE_HISTORY_FOUND or CONFIGURATION_ERROR.\n
    <content> (if <result> is CHARGE_HISTORY_FOUND) [{Array Dictionary}] containing charge history information.
    \tin_progress: {"vehicle", "id_vehicle_info", "charger", "time_start", "percentage_start"}
    \complete: {"vehicle", "id_vehicle_info", "charger", "time_start", "time_end", "percentage_start", "percentage_end", "amount_payable"}
    \all: {"vehicle", "id_vehicle_info", "charger", "time_start", "time_end", "percentage_start", "percentage_end", "amount_payable", "is_charge_finished"}
    """

    # get charge history
    if filter_by == 'in_progress':
        charge_history_out = get_charge_history_dict(
            column_names=['id_vehicle_info', 'id_charger',
                          'time_start', 'total_energy_drawn'],
            where_array=[['id_user_info', id_user_info_sanitised], ['is_charge_finished', False]])
    elif filter_by == 'complete':
        charge_history_out = get_charge_history_dict(
            column_names=['id_vehicle_info', 'id_charger', 'time_start',
                          'time_end', 'total_energy_drawn', 'amount_payable'],
            where_array=[['id_user_info', id_user_info_sanitised], ['is_charge_finished', True]])
    elif filter_by == 'all':
        charge_history_out = get_charge_history_dict(
            column_names=['id_vehicle_info', 'id_charger', 'time_start', 'time_end',
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
    charger_hash_map_out = db_charger.get_charger_hash_map(column_names=['name', 'latitude', 'longitude', 'address', 'currently_open',
                                                                         'pv_current_in', 'pv_energy_level', 'rate_current', 'rate_predicted',
                                                                         'active', 'last_updated', 'available_connector'],
                                                           where_array=[['active', True]])
    # check if empty or error (empty -> internal error)
    if charger_hash_map_out['result'] != db_service_code_master.HASHMAP_GENERIC_SUCCESS:
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
    Attempts to insert a charge history into the database. This method will also add an entry to "charge current",
    as this method is called when the user starts a charge.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CHARGE_HISTORY_CREATE_FAILURE or CHARGE_HISTORY_CREATE_SUCCESS.\n
    <reason> (if <result> is CHARGE_HISTORY_CREATE_FAILURE) [Array] Reason for failure.
    \t[ACCOUNT_NOT_FOUND, CHARGE_HISTORY_ALREADY_CHARGING, VEHICLE_NOT_FOUND, CHARGER_NOT_FOUND, CHARGE_HISTORY_INVALID_CHARGE_LEVEL]
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
    Attempts to finish an unfinished charge history. This method will also remove the corresponding "charge current" entry.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CHARGE_HISTORY_FINISH_FAILURE or CHARGE_HISTORY_FINISH_SUCCESS.\n
    <reason> (if <result> is CHARGE_HISTORY_FINISH_FAILURE) [Array] Reason for failure.
    \t[CHARGE_HISTORY_NOT_CHARGING]
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
