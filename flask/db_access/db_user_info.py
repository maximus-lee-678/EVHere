import datetime
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods

def create_user(input_username, input_password, input_email, input_full_name, input_phone_no):
    """
    Attempts to insert a new user into the database.\n
    Returns Dictionary with keys:\n
    <result> USER_INFO_CREATE_FAILURE or USER_INFO_CREATE_SUCCESS.\n
    <reason> (if <result> is USER_INFO_CREATE_FAILURE) [Array] Reason for failure.
    \t[reasons]:\n
    \t[USERNAME_INVALID_LENGTH, PASSWORD_INVALID_LENGTH, PASSWORD_INVALID_SYNTAX, 
    EMAIL_INVALID_LENGTH, EMAIL_INVALID_SYNTAX, ACCOUNT_ALREADY_EXISTS, PHONE_NUMBER_INVALID, FULL_NAME_INVALID_LENGTH]
    """

    contains_errors = False
    error_list = []

    # 1.1: input_username > check[length]
    if len(input_username) > 64 or len(input_username) == 0:
        contains_errors = True
        error_list.append(db_service_code_master.USERNAME_INVALID_LENGTH)
    # 1.2: sanitise username
    else:
        username = db_helper_functions.string_sanitise(input_username)

    # 2.1: password > check[length]
    if len(input_password) > 64 or len(input_password) == 0:
        contains_errors = True
        error_list.append(db_service_code_master.PASSWORD_INVALID_LENGTH)
    # 2.2: password > check[security level]
    elif not db_helper_functions.validate_password(input_password):
        contains_errors = True
        error_list.append(db_service_code_master.PASSWORD_INVALID_SYNTAX)
    # 2.3: hash password
    else:
        hashed_password = db_helper_functions.password_encrypt(input_password)

    # 3.1: email > check[length]
    if len(input_email) > 255 or len(input_email) == 0:
        contains_errors = True
        error_list.append(db_service_code_master.EMAIL_INVALID_LENGTH)
    # 3.2: email > check[syntax]
    elif not db_helper_functions.validate_email(input_email):
        contains_errors = True
        error_list.append(db_service_code_master.EMAIL_INVALID_SYNTAX)
    # 3.3: check if email exists
    else:
        email_response = get_user_id_by_email(input_email=input_email)
        if email_response['result'] == db_service_code_master.ACCOUNT_FOUND:
            contains_errors = True
            error_list.append(db_service_code_master.ACCOUNT_ALREADY_EXISTS)
        else:
            email = db_helper_functions.string_sanitise(input_email)

    # 4.1: phone_no > check[length & syntax]
    if not db_helper_functions.validate_phone_no(input_phone_no):
        contains_errors = True
        error_list.append(db_service_code_master.PHONE_NUMBER_INVALID)
    # 4.2: variable change (lol)
    else:
        phone_no = input_phone_no

    # 5.1: full_name > check[length]
    if len(input_full_name) > 255 or len(input_full_name) == 0:
        contains_errors = True
        error_list.append(db_service_code_master.FULL_NAME_INVALID_LENGTH)
    # 5.2: sanitise name
    else:
        full_name = db_helper_functions.string_sanitise(input_full_name)

    if contains_errors:
        return {'result': db_service_code_master.USER_INFO_CREATE_FAILURE, 'reason': error_list}

    # 6: previous checks passed, generate rest of the fields
    id = db_helper_functions.generate_uuid()
    created_at = datetime.datetime.now()
    modified_at = datetime.datetime.now()

    # 7: insert new user
    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    task = (id, username, hashed_password, email,
            full_name, phone_no, created_at, modified_at)
    cursor.execute('INSERT INTO user_info VALUES (?,?,?,?,?,?,?,?)', task)

    conn.commit()
    db_methods.close_connection(conn)

    return {'result': db_service_code_master.USER_INFO_CREATE_SUCCESS}


def login_user(input_email, input_password):
    """
    Takes an input email and password and verifies that it exists in the database.\n
    Returns Dictionary with keys:\n
    <result> LOGIN_FAILURE or LOGIN_SUCCESS.\n
    <reason> (if <result> is LOGIN_FAILURE) [Array] Reason for failure.
    \t[reasons]:\n
    \t[EMAIL_PASSWORD_INVALID]
    """

    # 1.1: email > check[length]
    if len(input_email) > 255:
        return {'result': db_service_code_master.LOGIN_FAILURE, 'reason': [db_service_code_master.EMAIL_PASSWORD_INVALID]}
    # 1.2: email > check[syntax]
    if not db_helper_functions.validate_email(input_email):
        return {'result': db_service_code_master.LOGIN_FAILURE, 'reason': [db_service_code_master.EMAIL_PASSWORD_INVALID]}
    # 1.3: sanitise email
    email = db_helper_functions.string_sanitise(input_email)

    # 2.1: get first row of email, if any. fields: password
    conn = db_methods.setup_connection()
    cursor = conn.cursor()
    task = (email,)
    cursor.execute('SELECT password FROM user_info WHERE email=?', task)
    row = cursor.fetchone()
    db_methods.close_connection(conn)
    if db_methods.check_fetchone_has_nothing(row):
        return {'result': db_service_code_master.LOGIN_FAILURE, 'reason': [db_service_code_master.EMAIL_PASSWORD_INVALID]}
    # 2.2: obtain account password hash
    password_hash_string = row[0]
    # 2.3: check if passwords match
    if db_helper_functions.password_check(input_password, password_hash_string):
        return {'result': db_service_code_master.LOGIN_SUCCESS}
    else:
        return {'result': db_service_code_master.LOGIN_FAILURE, 'reason': [db_service_code_master.EMAIL_PASSWORD_INVALID]}
    

def get_user_id_by_email(input_email):
    """
    Takes an input email verifies that it exists in the database.\n
    Returns Dictionary with keys:\n
    <result> ACCOUNT_NOT_FOUND or ACCOUNT_FOUND.\n
    <content> (if <result> is ACCOUNT_FOUND) =Value= containing user_id.
    """

    # sanitise email
    email = db_helper_functions.string_sanitise(input_email)

    # get user_id from email
    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    task = (email,)
    cursor.execute('SELECT id FROM user_info WHERE email=?', task)

    row = cursor.fetchone()
    db_methods.close_connection(conn)

    if row is None:
        return {"result": db_service_code_master.ACCOUNT_NOT_FOUND}
    else:
        return {"result": db_service_code_master.ACCOUNT_FOUND, "content": row[0]}
