# Universal imports
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods

# Other db_access imports
import db_access.db_user_info as db_user_info
import db_access.db_charger as db_charger


def get_favourite_charger_id(input_user_id, input_charger_id):
    """
    Attempts to retrieve one favourite charger entry from the database.\n
    Returns Dictionary with keys:\n
    <result> FAVOURITE_CHARGERS_NOT_FOUND or FAVOURITE_CHARGERS_FOUND.\n
    <content> (if <result> is FAVOURITE_CHARGERS_FOUND) =Value= containing favourite charger id.
    """

    # sanitise inputs
    user_id = db_helper_functions.string_sanitise(input_user_id)
    charger_id = db_helper_functions.string_sanitise(input_charger_id)

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    task = (user_id, charger_id)
    cursor.execute(
        'SELECT id FROM favourited_chargers WHERE id_user_info=? AND id_charger=?', task)

    row = cursor.fetchone()
    db_methods.close_connection(conn)

    if db_methods.check_fetchone_has_nothing(row):
        return {'result': db_service_code_master.FAVOURITE_CHARGERS_NOT_FOUND}

    return {'result': db_service_code_master.FAVOURITE_CHARGERS_FOUND, 'content': row[0]}


def modify_favourite_charger(input_email, input_charger_id, input_action):
    """
    Attempts to add or remove one favourite charger entry to or from the database.\n
    Returns Dictionary with keys:\n
    <result> FAVOURITE_CHARGER_MODIFY_SUCCESS or FAVOURITE_CHARGER_MODIFY_FAILURE.\n
    <reason> (if <result> is FAVOURITE_CHARGER_MODIFY_FAILURE) [Array] Reason for failure.
    \t[reasons]:\n
    [ACCOUNT_NOT_FOUND, CHARGER_NOT_FOUND, FAVOURITE_CHARGER_MODIFY_ILLEGAL_OPERATION, FAVOURITE_CHARGER_MODIFY_INVALID_OPERATION]
    """

    contains_errors = False
    error_list = []

    # 1.1: check if email exists
    email_response = db_user_info.get_user_id_by_email(input_email=input_email)
    if email_response['result'] == db_service_code_master.ACCOUNT_NOT_FOUND:
        contains_errors = True
        error_list.append(email_response['result'])
    # 1.2: store user id
    else:
        user_id = email_response['content']

    # 2.1: check if charger exists
    charger_response = db_charger.get_one_charger(input_charger_id)
    if charger_response['result'] == db_service_code_master.CHARGER_NOT_FOUND:
        contains_errors = True
        error_list.append(charger_response['result'])
    # 2.2: store charger id (response contains sanitised id)
    else:
        charger_id = charger_response['content']['id']

    ##### Query formation START #####
    # 3a: Add favourite
    if input_action == 'add':
        # 3a.1: ensure charger not already favourited
        if get_favourite_charger_id(user_id, charger_id)['result'] == db_service_code_master.FAVOURITE_CHARGERS_FOUND:
            contains_errors = True
            error_list.append(db_service_code_master.FAVOURITE_CHARGER_MODIFY_ILLEGAL_OPERATION)
        # 3a.2: Insert Query / Form Parameters
        else:
            query = 'INSERT INTO favourited_chargers VALUES (?,?,?)'
            id = db_helper_functions.generate_uuid()
            task = (id, user_id, charger_id)
    # 3b: Remove favourite
    elif input_action == 'remove':
        # 3b.1: ensure charger already favourited
        if get_favourite_charger_id(user_id, charger_id)['result'] == db_service_code_master.FAVOURITE_CHARGERS_NOT_FOUND:
            contains_errors = True
            error_list.append(db_service_code_master.FAVOURITE_CHARGER_MODIFY_ILLEGAL_OPERATION)
        # 3b.2: Delete Query / Form Parameters
        else:
            query = 'DELETE FROM favourited_chargers WHERE id_user_info=? AND id_charger=?'
            task = (user_id, charger_id)
    # 3c: Invalid Stance
    else:
        contains_errors = True
        error_list.append(db_service_code_master.FAVOURITE_CHARGER_MODIFY_INVALID_OPERATION)
    ##### Query formation END #####

    if contains_errors:
        return {'result': db_service_code_master.FAVOURITE_CHARGER_MODIFY_FAILURE, 'reason': error_list}
    
    # 4: add / remove entry
    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    cursor.execute(query, task)

    conn.commit()
    db_methods.close_connection(conn)

    return {'result': db_service_code_master.FAVOURITE_CHARGER_MODIFY_SUCCESS}
