import db_methods
import helper_functions

import db_user_info
import db_charger

FAVOURITE_CHARGER_NOT_FOUND = 100
FAVOURITE_CHARGER_FOUND = 101
MODIFY_SUCCESS = 102
MODIFY_BAD_EMAIL = 103
MODIFY_BAD_CHARGER_ID = 104
MODIFY_INVALID_OPERATION = 105
MODIFY_BAD_ACTION = 106

service_code_dict = {
    FAVOURITE_CHARGER_NOT_FOUND: "Favourite charger found.",
    FAVOURITE_CHARGER_FOUND: "Favourite charger not found.",
    MODIFY_SUCCESS: "Favourite modified.",
    MODIFY_BAD_EMAIL: "Invalid email sent.",
    MODIFY_BAD_CHARGER_ID: "Invalid charger id specified.",
    MODIFY_INVALID_OPERATION: "Already favourited/removed.",
    MODIFY_BAD_ACTION: "Invalid operation type."
}


def get_favourite_charger_one(input_user_id, input_charger_id):
    """
    Attempts to retrieve one favourite charger entry from the database.\n
    Returns Dictionary with keys:\n
    <result> FAVOURITE_CHARGER_NOT_FOUND or FAVOURITE_CHARGER_FOUND.\n
    <content> (if <result> is FAVOURITE_CHARGER_FOUND) Array containing favourite charger information.
    """

    # sanitise inputs
    user_id = helper_functions.string_sanitise(input_user_id)
    charger_id = helper_functions.string_sanitise(input_charger_id)

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    task = (user_id, charger_id)
    cursor.execute(
        'SELECT * FROM favourited_chargers WHERE id_user_info=? AND id_charger=?', task)

    row = cursor.fetchone()
    db_methods.close_connection(conn)

    if db_methods.check_fetchone_has_nothing(row):
        return {'result': FAVOURITE_CHARGER_NOT_FOUND}

    return {'result': FAVOURITE_CHARGER_FOUND, 'content': row}


def modify_favourite_charger(input_email, input_charger_id, input_action):
    """
    Attempts to add or remove one favourite charger entry to or from the database.\n
    Returns Dictionary with keys:\n
    <result> MODIFY_BAD_EMAIL, MODIFY_BAD_CHARGER_ID, MODIFY_INVALID_OPERATION, MODIFY_BAD_ACTION or MODIFY_SUCCESS.
    """

    # 1.1: check if email exists
    user_response = db_user_info.get_user_id_by_email(input_email=input_email)
    if user_response['result'] == db_user_info.ACCOUNT_NOT_FOUND:
        return {'result': MODIFY_BAD_EMAIL}
    # 1.2: store user id
    user_id = user_response['content']

    # 2.1: check if charger exists
    charger_response = db_charger.get_one_charger(input_charger_id)
    if charger_response['result'] == db_charger.CHARGER_NOT_FOUND:
        return {'result': MODIFY_BAD_CHARGER_ID}
    # 2.2: store charger id (response contains sanitised id)
    charger_id = charger_response['content'][0]

    ##### Query formation START #####
    # 3a: Add favourite
    if input_action == 'add':
        # 3a.1: ensure charger not already favourited
        if get_favourite_charger_one(user_id, charger_id)['result'] == FAVOURITE_CHARGER_FOUND:
            return {'result': MODIFY_INVALID_OPERATION}

        # 3a.2: Insert Query / Form Parameters
        query = 'INSERT INTO favourited_chargers VALUES (?,?,?)'
        id = helper_functions.generate_uuid()
        task = (id, user_id, charger_id)
    # 3b: Remove favourite
    elif input_action == 'remove':
        # 3b.1: ensure charger already favourited
        if get_favourite_charger_one(user_id, charger_id)['result'] == FAVOURITE_CHARGER_NOT_FOUND:
            return {'result': MODIFY_INVALID_OPERATION}

        # 3b.2: Delete Query / Form Parameters
        query = 'DELETE FROM favourited_chargers WHERE id_user_info=? AND id_charger=?'
        task = (user_id, charger_id)
    # 3c: Illegal Stance
    else:
        return {'result': MODIFY_BAD_ACTION}
    ##### Query formation END #####

    # 4: add / remove entry
    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    cursor.execute(query, task)

    conn.commit()
    db_methods.close_connection(conn)

    return {'result': MODIFY_SUCCESS}
