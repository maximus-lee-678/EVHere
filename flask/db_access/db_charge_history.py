# Universal imports
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods

# Other db_access imports
import db_access.db_vehicle as db_vehicle
import db_access.db_charger as db_charger
import db_access.db_charge_current as db_charge_current


def get_charge_history_by_user_id(id_user_info_sanitised, filter_by):
    """
    Retrieve's a user's charge history.
    \tfilter_by >> in_progress, complete, all\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CHARGE_HISTORY_NOT_FOUND, CHARGE_HISTORY_FOUND or CONFIGURATION_ERROR.\n
    <content> (if <result> is CHARGE_HISTORY_FOUND) [{Array Dictionary}] containing charge history information.
    \t{"id", "name", "model", "vehicle_sn", "connector_type"}
    """

    ##### Query formation START #####
    if filter_by == 'in_progress':
        query = 'SELECT * FROM charge_history WHERE id_user_info=? AND is_charge_finished=False'
    elif filter_by == 'complete':
        query = 'SELECT * FROM charge_history WHERE id_user_info=? AND is_charge_finished=True'
    elif filter_by == 'all':
        query = 'SELECT * FROM charge_history WHERE id_user_info=?'
    else:
        return {'result': db_service_code_master.CONFIGURATION_ERROR}
    ##### Query formation END #####

    task = (id_user_info_sanitised,)

    select = db_methods.safe_select(query=query, task=task, get_type='one')
    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.CHARGE_HISTORY_NOT_FOUND}

    key_values = {"id": select['content'][0], "id_user_info": select['content'][1], "id_vehicle_info": select['content'][2],
                  "id_charger": select['content'][3], "time_start": select['content'][4], "time_end": select['content'][5],
                  "percentage_start": select['content'][6], "percentage_end": select['content'][7],
                  "amount_payable": select['content'][8], "is_charge_finished": False if select['content'][9] == 0 else True}

    return {'result': db_service_code_master.CHARGE_HISTORY_FOUND,
            'content': key_values}


def get_charge_history_by_id(id_charge_history):
    """
    Retrieve's a charge history entry by id.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CHARGE_HISTORY_NOT_FOUND or CHARGE_HISTORY_FOUND.\n
    <content> (if <result> is CHARGE_HISTORY_FOUND) {Dictionary} containing charge history information.
    \t{"id", "name", "model", "vehicle_sn", "connector_type"}
    """

    # sanitise input
    id = db_helper_functions.string_sanitise(id_charge_history)

    query = 'SELECT * FROM charge_history WHERE id=?'
    task = (id,)

    select = db_methods.safe_select(query=query, task=task, get_type='all')
    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.CHARGE_HISTORY_NOT_FOUND}
    
    key_values = []
    for row in select['content']:
        key_values.append({"id": row[0], "id_user_info": row[1], "id_vehicle_info": row[2], "id_charger": row[3],
                           "time_start": row[4], "time_end": row[5], "percentage_start": row[6],
                           "percentage_end": row[7], "amount_payable": row[8], "is_charge_finished": False if row[9] == 0 else True})

    return {'result': db_service_code_master.CHARGE_HISTORY_FOUND,
            'content': key_values}


def add_charge_history_initial(id_user_info_sanitised, id_vehicle_info_input, id_charger_input, battery_percentage_input):
    """
    Attempts to insert a charge history into the database. This method will also add an entry to "charge current",
    as this method is called when the user starts a charge.\n
    Returns Dictionary with keys:\n
    <result> CHARGE_HISTORY_CREATE_FAILURE or CHARGE_HISTORY_CREATE_SUCCESS.\n
    <reason> (if <result> is CHARGE_HISTORY_CREATE_FAILURE) [Array] Reason for failure.
    \t[INTERNAL_ERROR, ACCOUNT_NOT_FOUND, CHARGE_HISTORY_ALREADY_CHARGING, VEHICLE_NOT_FOUND, CHARGER_NOT_FOUND, CHARGE_HISTORY_INVALID_CHARGE_LEVEL]
    """

    contains_errors = False
    error_list = []

    # 1: check if user is already charging a vehicle
    charger_response = get_charge_history_by_user_id(
        id_user_info_sanitised=id_user_info_sanitised, filter_by="in_progress")
    if charger_response['result'] != db_service_code_master.CHARGE_HISTORY_NOT_FOUND:
        contains_errors = True
        error_list.append(
            db_service_code_master.CHARGE_HISTORY_ALREADY_CHARGING)

    # 2.1: check if vehicle exists
    vehicle_response = db_vehicle.get_vehicle_by_id(
        id_vehicle_input=id_vehicle_info_input)
    if vehicle_response['result'] == db_service_code_master.VEHICLE_NOT_FOUND:
        contains_errors = True
        error_list.append(vehicle_response['result'])
    # 2.2: store vehicle id (response contains sanitised id)
    else:
        id_vehicle_info_sanitised = vehicle_response['content']['id']

    # 3.1: check if charger exists
    charger_response = db_charger.get_one_charger(
        id_charger_input=id_charger_input)
    if charger_response['result'] != db_service_code_master.CHARGER_FOUND:
        contains_errors = True
        error_list.append(charger_response['result'])
    # 3.2: store charger id (response contains sanitised id)
    else:
        id_charger_sanitised = charger_response['content']['id']

    # 4.1: check if battery percentage is digit
    if battery_percentage_input.isdigit():
        # 4.2: store battery percentage, check if between 0 - 100
        percentage_start = int(battery_percentage_input)
        if percentage_start > 100 or percentage_start < 0:
            contains_errors = True
            error_list.append(
                db_service_code_master.CHARGE_HISTORY_INVALID_CHARGE_LEVEL)
    else:
        contains_errors = True
        error_list.append(
            db_service_code_master.CHARGE_HISTORY_INVALID_CHARGE_LEVEL)

    if contains_errors:
        return {'result': db_service_code_master.CHARGE_HISTORY_CREATE_FAILURE, 'reason': error_list}

    # 5: previous checks passed, generate rest of the fields
    id_charge_history = db_helper_functions.generate_uuid()
    time_start = db_helper_functions.generate_time_now()

    # 6: insert new charge history entry
    query = """
    INSERT INTO charge_history 
    (id, id_user_info, id_vehicle_info, id_charger, time_start, percentage_start, is_charge_finished)
    VALUES (?,?,?,?,?,?,?) 
    """
    task = (id_charge_history, id_user_info_sanitised, id_vehicle_info_sanitised, id_charger_sanitised,
            time_start, percentage_start, False)
    
    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.CHARGE_CURRENT_CREATE_FAILURE, 'reason': [db_service_code_master.INTERNAL_ERROR]}

    # 7: insert new charge current entry
    charge_current_response = db_charge_current.add_charge_current(
        id_charge_history, percentage_start)
    if charge_current_response['result'] != db_service_code_master.CHARGE_CURRENT_CREATE_SUCCESS:
        # destroy charge history entry
        # TODO
        return {'result': db_service_code_master.CHARGE_HISTORY_CREATE_FAILURE,
                'reason': charge_current_response['result']}

    return {'result': db_service_code_master.CHARGE_HISTORY_CREATE_SUCCESS}
