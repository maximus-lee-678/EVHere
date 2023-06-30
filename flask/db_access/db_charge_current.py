# Universal imports
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods

# Other db_access imports
import db_access.db_charge_history as db_charge_history


def add_charge_current(id_charge_history, percentage_current):
    """
    Inserts a charge current entry into the database. This function assumes input is legal, as it cannot be called directly.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR or CHARGE_CURRENT_CREATE_SUCCESS.
    """

    # generate rest of the fields
    id = db_helper_functions.generate_uuid()
    last_updated = db_helper_functions.generate_time_now()

    query = 'INSERT INTO charge_current VALUES (?,?,?,?)'
    task = (id, id_charge_history, percentage_current, last_updated)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result':db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.CHARGE_CURRENT_CREATE_SUCCESS}


def get_charge_current_by_user_id_verbose(id_user_info_sanitised):
    """
    Attempts to retrieve a charge current entry based on user id. 
    The entry is also joined with charge history and vehicle details.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CHARGE_CURRENT_NOT_FOUND or CHARGE_CURRENT_FOUND.\n
    <content> (if <result> is CHARGE_CURRENT_FOUND) {Dictionary} containing charge current information.
    \t{"vehicle_name", "vehicle_sn", "percentage_start", "percentage_current", "charger_name", 
    \t"charger_latitude", "charger_longitude", "time_start", "last_updated"}
    """

    query = """
    SELECT vi.name AS vehicle_name, vi.vehicle_sn,
    ch.percentage_start, cc.percentage_current, 
    c.name AS charger_name, c.latitude AS charger_latitude, c.longitude AS charger_longitude,
    ch.time_start, cc.last_updated
    FROM charge_current AS cc
    LEFT JOIN charge_history AS ch ON ch.id=cc.id_charge_history
    LEFT JOIN vehicle_info AS vi ON vi.id=ch.id_vehicle_info
    LEFT JOIN charger AS c on c.id=ch.id_charger
    WHERE ch.id_user_info=?
    """
    task = (id_user_info_sanitised,)
    
    select = db_methods.safe_select(query=query, task=task, get_type='one')
    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.CHARGE_CURRENT_NOT_FOUND}
    
    key_values = {"vehicle_name": select['content'][0], "vehicle_sn": select['content'][1], "percentage_start": select['content'][2],
                   "percentage_current": select['content'][3], "charger_name": select['content'][4], "charger_latitude": select['content'][5],
                   "charger_longitude": select['content'][6], "time_start": select['content'][7], "last_updated": select['content'][8]}

    return {'result': db_service_code_master.CHARGE_CURRENT_FOUND, 'content': key_values}


def update_charge_current(id_charge_history, percentage_current):
    pass


def remove_charge_current(id_charge_history):
    """
    Removes a charge current entry from the database. This function assumes input is legal, as it cannot be called directly.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR or CHARGE_CURRENT_REMOVE_SUCCESS.
    """
    query = 'DELETE FROM charge_current WHERE id_charge_history=?'
    task = (id_charge_history,)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.CHARGE_CURRENT_REMOVE_SUCCESS}
