# Universal imports
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods

# Other db_access imports
import db_access.db_charger as db_charger


def get_favourite_charger_id(id_user_info_sanitised, id_charger_input):
    """
    Attempts to retrieve one favourite charger entry from the database.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, FAVOURITE_CHARGERS_NOT_FOUND or FAVOURITE_CHARGERS_FOUND.\n
    <content> (if <result> is FAVOURITE_CHARGERS_FOUND) =Value= containing favourite charger id.
    """

    # sanitise inputs
    id_charger_sanitised = db_helper_functions.string_sanitise(
        id_charger_input)

    query = 'SELECT id FROM favourited_chargers WHERE id_user_info=? AND id_charger=?'
    task = (id_user_info_sanitised, id_charger_sanitised)

    select = db_methods.safe_select(query=query, task=task, get_type='one')

    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.FAVOURITE_CHARGERS_NOT_FOUND}

    return {'result': db_service_code_master.FAVOURITE_CHARGERS_FOUND, 'content': select['content'][0]}


def add_favourite_charger(id_user_info_sanitised, id_charger_input):
    """
    Attempts to add one favourite charger entry to the database.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, FAVOURITE_CHARGER_MODIFY_SUCCESS or FAVOURITE_CHARGER_MODIFY_FAILURE.\n
    <reason> (if <result> is FAVOURITE_CHARGER_MODIFY_FAILURE) [Array] Reason for failure.
    \t[reasons]:\n
    [CHARGER_NOT_FOUND, FAVOURITE_CHARGER_DUPLICATE_ENTRY]
    """

    contains_errors = False
    error_list = []

    # 1.1: check if charger exists
    charger_response = db_charger.get_one_charger(id_charger_input)
    if charger_response['result'] != db_service_code_master.CHARGER_FOUND:
        contains_errors = True
        error_list.append(charger_response['result'])
    # 1.2: store charger id (response contains sanitised id)
    else:
        id_charger_sanitised = charger_response['content']['id']

    # 2.1: ensure charger not already favourited (no dupes)
    if get_favourite_charger_id(id_user_info_sanitised, id_charger_sanitised)['result'] != db_service_code_master.FAVOURITE_CHARGERS_NOT_FOUND:
        contains_errors = True
        error_list.append(
            db_service_code_master.FAVOURITE_CHARGER_DUPLICATE_ENTRY)

    if contains_errors:
        return {'result': db_service_code_master.FAVOURITE_CHARGER_MODIFY_FAILURE, 'reason': error_list}

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
    Attempts to remove one favourite charger entry from the database. A lot less stringent than add, as it affects nothing if entry isn't found.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, FAVOURITE_CHARGER_MODIFY_SUCCESS or FAVOURITE_CHARGER_MODIFY_FAILURE.\n
    <reason> (if <result> is FAVOURITE_CHARGER_MODIFY_FAILURE) [Array] Reason for failure.
    \t[reasons]:\n
    [FAVOURITE_CHARGERS_NOT_FOUND]
    """

    id_charger_sanitised = db_helper_functions.string_sanitise(
        id_charger_input)

    query = 'DELETE FROM favourited_chargers WHERE id_user_info=? AND id_charger=?'
    task = (id_user_info_sanitised, id_charger_sanitised)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if transaction['rows_affected'] != 1:
        return {'result': db_service_code_master.FAVOURITE_CHARGER_MODIFY_FAILURE, 'reason': [db_service_code_master.FAVOURITE_CHARGERS_NOT_FOUND]}

    return {'result': db_service_code_master.FAVOURITE_CHARGER_MODIFY_SUCCESS}
