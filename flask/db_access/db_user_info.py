import datetime
import db_access.db_helper_functions as db_helper_functions
import db_access.db_methods as db_methods

# C represent
ACCOUNT_ALREADY_EXISTS = 1
USERNAME_INVALID_LENGTH = 2
PASSWORD_INVALID_LENGTH = 3
PASSWORD_INVALID_SYNTAX = 4
EMAIL_INVALID_LENGTH = 5
EMAIL_INVALID_SYNTAX = 6
PHONE_NUMBER_INVALID = 7
FULL_NAME_INVALID_LENGTH = 8

CREATE_SUCCESS = 100
CREATE_FAILURE = 101
LOGIN_SUCCESS = 102
LOGIN_FAILURE = 103
EMAIL_PASSWORD_INVALID = 104
ACCOUNT_FOUND = 105
ACCOUNT_NOT_FOUND = 106

service_code_dict = {
    ACCOUNT_ALREADY_EXISTS: "Account already exists in system.",
    USERNAME_INVALID_LENGTH: "Username is of invalid length.",
    PASSWORD_INVALID_LENGTH: "Password is of invalid length.",
    PASSWORD_INVALID_SYNTAX: "Password does not meet complexity requirements.",
    EMAIL_INVALID_LENGTH: "Email is of invalid length.",
    EMAIL_INVALID_SYNTAX: "Email is not valid.",
    PHONE_NUMBER_INVALID: "Phone number is not valid.",
    FULL_NAME_INVALID_LENGTH: "Full name is of invalid length.",
    CREATE_SUCCESS: "Account successfully created!",
    CREATE_FAILURE: "Could not create account.",
    LOGIN_SUCCESS: "Login successful!",
    LOGIN_FAILURE: "Login failed.",
    EMAIL_PASSWORD_INVALID: "Email or Password is incorrect.",
    ACCOUNT_FOUND: "Account found.",
    ACCOUNT_NOT_FOUND: "Account not found."
}


def create_user(input_username, input_password, input_email, input_full_name, input_phone_no):
    """
    Attempts to insert a new user into the database.\n
    Returns Dictionary with keys:\n
    <result> CREATE_FAILURE or CREATE_SUCCESS.\n
    <reason> (if <result> is CREATE_FAILURE) Reason for failure. (IN ARRAY FORMAT)
    """

    contains_errors = False
    error_list = []

    # 1.1: input_username > check[length]
    if len(input_username) > 64 or len(input_username) == 0:
        contains_errors = True
        error_list.append(USERNAME_INVALID_LENGTH)
    # 1.2: sanitise username
    else:
        username = db_helper_functions.string_sanitise(input_username)

    # 2.1: password > check[length]
    if len(input_password) > 64 or len(input_password) == 0:
        contains_errors = True
        error_list.append(PASSWORD_INVALID_LENGTH)
    # 2.2: password > check[security level]
    elif not db_helper_functions.validate_password(input_password):
        contains_errors = True
        error_list.append(PASSWORD_INVALID_SYNTAX)
    # 2.3: hash password
    else:
        hashed_password = db_helper_functions.password_encrypt(input_password)

    # 3.1: email > check[length]
    if len(input_email) > 255 or len(input_email) == 0:
        contains_errors = True
        error_list.append(EMAIL_INVALID_LENGTH)
    # 3.2: email > check[syntax]
    elif not db_helper_functions.validate_email(input_email):
        contains_errors = True
        error_list.append(EMAIL_INVALID_SYNTAX)
    else:
        # 3.3: sanitise email
        email = db_helper_functions.string_sanitise(input_email)
        # 3.4: email > check[already exists]
        conn = db_methods.setup_connection()
        cursor = conn.cursor()
        task = (email,)
        cursor.execute('SELECT * FROM user_info WHERE email=?', task)
        row = cursor.fetchone()
        db_methods.close_connection(conn)
        if not db_methods.check_fetchone_has_nothing(row):
            contains_errors = True
            error_list.append(ACCOUNT_ALREADY_EXISTS)

    # 4.1: phone_no > check[length & syntax]
    if not db_helper_functions.validate_phone_no(input_phone_no):
        contains_errors = True
        error_list.append(PHONE_NUMBER_INVALID)
    # 4.2: variable change (lol)
    else:
        phone_no = input_phone_no

    # 5.1: full_name > check[length]
    if len(input_full_name) > 255 or len(input_full_name) == 0:
        contains_errors = True
        error_list.append(FULL_NAME_INVALID_LENGTH)
    # 5.2: sanitise name
    else:
        full_name = db_helper_functions.string_sanitise(input_full_name)

    if contains_errors:
        return {'result': CREATE_FAILURE, 'reason': error_list}

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

    return {'result': CREATE_SUCCESS}


def login_user(input_email, input_password):
    """
    Takes an input email and password and verifies that it exists in the database.\n
    Returns Dictionary with keys:\n
    <result> LOGIN_FAILURE or LOGIN_SUCCESS.\n
    <reason> (if <result> is LOGIN_FAILURE) Reason for failure.
    """

    # 1.1: email > check[length]
    if len(input_email) > 255:
        return {'result': LOGIN_FAILURE, 'reason': EMAIL_PASSWORD_INVALID}
    # 1.2: email > check[syntax]
    if not db_helper_functions.validate_email(input_email):
        return {'result': LOGIN_FAILURE, 'reason': EMAIL_PASSWORD_INVALID}
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
        return {'result': LOGIN_FAILURE, 'reason': EMAIL_PASSWORD_INVALID}
    # 2.2: obtain account password hash
    password_hash_string = row[0]
    # 2.3: check if passwords match
    if db_helper_functions.password_check(input_password, password_hash_string):
        return {'result': LOGIN_SUCCESS}
    else:
        return {'result': LOGIN_FAILURE, 'reason': EMAIL_PASSWORD_INVALID}


def get_user_id_by_email(input_email):
    """
    Takes an input email verifies that it exists in the database.\n
    Returns Dictionary with keys:\n
    <result> ACCOUNT_NOT_FOUND or ACCOUNT_FOUND.\n
    <content> (if <result> is ACCOUNT_FOUND) Value containing user_id.
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
        return {"result": ACCOUNT_NOT_FOUND}
    else:
        return {"result": ACCOUNT_FOUND, "content": row[0]}