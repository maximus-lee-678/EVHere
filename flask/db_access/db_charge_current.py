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


def get_charge_current_by_user_id(id_user_info_sanitised):
    """
    Attempts to retrieve a charge current entry based on user id.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CHARGE_CURRENT_NOT_FOUND or CHARGE_CURRENT_FOUND.\n
    <content> (if <result> is CHARGE_CURRENT_FOUND) {Dictionary} containing charge current information.
    \t{"id", "id_charge_history", "percentage_current", "last_updated"}
    """

    # check if user has a charge history entry where is_charge_finished is false
    charge_history_response = db_charge_history.get_charge_history_by_user_id(
        id_user_info_sanitised=id_user_info_sanitised, filter_by='in_progress')
    if charge_history_response['result'] != db_service_code_master.CHARGE_HISTORY_FOUND:
        return {'result': db_service_code_master.CHARGE_CURRENT_NOT_FOUND}

    # store charge history id
    id_charge_history = charge_history_response['content']['id']

    query = 'SELECT * FROM charge_current WHERE id_charge_history=?'
    task = (id_charge_history,)
    
    select = db_methods.safe_select(query=query, task=task, get_type='one')
    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    
    key_values = {"id": select['content'][0], "id_charge_history": select['content'][1],
                  "percentage_current": select['content'][2], "last_updated": select['content'][3]}

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
