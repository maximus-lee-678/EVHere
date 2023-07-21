# Universal imports
import copy
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods
import db_access.db_universal as db_universal

# Other db_access imports
#

# Generics:
column_sql_translations = {'id': 'id', 'username': 'username', 'password': 'password', 'email': 'email',
                           'full_name': 'full_name', 'phone_no': 'phone_no', 'created_at': 'created_at', 'modified_at': 'modified_at'}
column_names_all = ['id', 'username', 'password', 'email',
                    'full_name', 'phone_no', 'created_at', 'modified_at']
trailing_query = """
FROM user_info
"""


def get_user_info_hash_map(column_names=None, where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'username', 'password', 'email', 'full_name', 'phone_no', 'created_at', 'modified_at']\n
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


def get_user_info_dict(column_names=None, where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'username', 'password', 'email', 'full_name', 'phone_no', 'created_at', 'modified_at']\n
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


def create_user(username_input, password_input, email_input, full_name_input, phone_no_input):
    """
    Attempts to insert a new user into the database.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, USER_INFO_CREATE_FAILURE or USER_INFO_CREATE_SUCCESS.\n
    <reason> (if <result> is USER_INFO_CREATE_FAILURE) [Array] Reason for failure.
    \t[USERNAME_INVALID_LENGTH, PASSWORD_INVALID_LENGTH, PASSWORD_INVALID_SYNTAX,
    EMAIL_INVALID_LENGTH, EMAIL_INVALID_SYNTAX, ACCOUNT_ALREADY_EXISTS, PHONE_NUMBER_INVALID, FULL_NAME_INVALID_LENGTH]
    """

    contains_errors = False
    error_list = []

    user_info_out = validate_user_info(username_input=username_input, password_input=password_input,
                                       email_input=email_input, full_name_input=full_name_input, phone_no_input=phone_no_input)

    if user_info_out['result'] == db_service_code_master.USER_INFO_INVALID:
        contains_errors = True
        error_list = user_info_out['reason']
    else:
        # check for email duplicate
        user_info_dict_out = get_user_info_dict(column_names=['id'],
                                                where_array=[['email', user_info_out['content']['email_sanitised']]])
        if user_info_dict_out['result'] == db_service_code_master.SELECT_GENERIC_SUCCESS:
            contains_errors = True
            error_list.append(db_service_code_master.ACCOUNT_ALREADY_EXISTS)
        if user_info_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
            return {'result': db_service_code_master.INTERNAL_ERROR}

    if contains_errors:
        return {'result': db_service_code_master.USER_INFO_CREATE_FAILURE,
                'reason': error_list}

    # checks passed, generate rest of the fields
    id = db_helper_functions.generate_uuid()
    created_at = db_helper_functions.generate_time_now()
    modified_at = db_helper_functions.generate_time_now()

    # insert new user
    query = 'INSERT INTO user_info VALUES (?,?,?,?,?,?,?,?)'
    task = (id, user_info_out['content']['username_sanitised'], user_info_out['content']['password_hashed'],
            user_info_out['content']['email_sanitised'], user_info_out['content']['full_name_sanitised'],
            user_info_out['content']['phone_no_sanitised'], created_at, modified_at)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.USER_INFO_CREATE_SUCCESS}


def get_user_info_by_user_id(id_user_info_sanitised):
    """
    """

    user_info_dict_out = get_user_info_dict(column_names=['username', 'email', 'full_name', 'phone_no', 'created_at', 'modified_at'],
                                            where_array=[['id', id_user_info_sanitised]])
    # check if empty or error
    if user_info_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.ACCOUNT_NOT_FOUND}
    if user_info_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return user_info_dict_out

    return {'result': db_service_code_master.ACCOUNT_FOUND,
            'content': user_info_dict_out['content'][0]}


def update_user(id_user_info_sanitised, username_input, password_input, email_input, full_name_input, phone_no_input):
    """
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, USER_INFO_UPDATE_FAILURE or USER_INFO_UPDATE_SUCCESS.\n
    <reason> (if <result> is USER_INFO_UPDATE_FAILURE) [Array] Reason for failure.
    \t[USERNAME_INVALID_LENGTH, PASSWORD_INVALID_LENGTH, PASSWORD_INVALID_SYNTAX,
    EMAIL_INVALID_LENGTH, EMAIL_INVALID_SYNTAX, ACCOUNT_ALREADY_EXISTS, PHONE_NUMBER_INVALID, FULL_NAME_INVALID_LENGTH, ACCOUNT_NOT_FOUND]\n
    <content> (if <result> is USER_INFO_UPDATE_SUCCESS) Sanitised email string.
    """

    contains_errors = False
    error_list = []

    user_info_out = validate_user_info(username_input=username_input, password_input=password_input,
                                       email_input=email_input, full_name_input=full_name_input, phone_no_input=phone_no_input)

    if user_info_out['result'] == db_service_code_master.USER_INFO_INVALID:
        contains_errors = True
        error_list = user_info_out['reason']
    else:
        # check for email duplicate, but ignore if self
        user_info_dict_out = get_user_info_dict(column_names=['id'],
                                                where_array=[['email', user_info_out['content']['email']],
                                                             ['id', id_user_info_sanitised, 'NOT']])
        if user_info_dict_out['result'] == db_service_code_master.SELECT_GENERIC_SUCCESS:
            contains_errors = True
            error_list.append(db_service_code_master.ACCOUNT_ALREADY_EXISTS)
        if user_info_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
            return {'result': db_service_code_master.INTERNAL_ERROR}

    if contains_errors:
        return {'result': db_service_code_master.USER_INFO_UPDATE_FAILURE,
                'reason': error_list}
    
    query = f"""
    UPDATE user_info SET {', '.join(f'{key}=?' for key in user_info_out['content'].keys())}, modified_at=?
    WHERE id=?
    """
    task = tuple(value for value in user_info_out['content'].values()) + (db_helper_functions.generate_time_now(), id_user_info_sanitised)

    print(query)
    print(task)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if transaction['rows_affected'] != 1:
        return {'result': db_service_code_master.USER_INFO_UPDATE_FAILURE, 'reason': [db_service_code_master.ACCOUNT_NOT_FOUND]}

    return {'result': db_service_code_master.USER_INFO_UPDATE_SUCCESS, 'content': user_info_out['content']['email']}


def validate_user_info(username_input=None, password_input=None, email_input=None, full_name_input=None, phone_no_input=None):
    """
    Validates, sanitises, hashes, the whole lot (user info).\n
    Returns Dictionary with keys:\n
    <result> USER_INFO_INVALID or USER_INFO_VALID.\n
    <reason> (if <result> is USER_INFO_INVALID) [Array] Reason for failure.\n
    \t[USERNAME_INVALID_LENGTH, PASSWORD_INVALID_LENGTH, PASSWORD_INVALID_SYNTAX,
    EMAIL_INVALID_LENGTH, EMAIL_INVALID_SYNTAX, ACCOUNT_ALREADY_EXISTS, PHONE_NUMBER_INVALID, FULL_NAME_INVALID_LENGTH]\n
    <content> (if <result> is USER_INFO_VALID) {Dictionary} containing ready-to-use fields.\n
    \t{username, password, email, phone_no, full_name}\n
    \tReturns only fields it is provided with.
    """

    contains_errors = False
    error_list = []
    output_dict = {}

    if username_input != None:
        if len(username_input) > 64 or len(username_input) <= 0:
            contains_errors = True
            error_list.append(db_service_code_master.USERNAME_INVALID_LENGTH)
        elif not contains_errors:
            output_dict.update(
                {'username': db_helper_functions.string_sanitise(username_input)})

    if password_input != None:
        if len(password_input) > 64 or len(password_input) <= 0:
            contains_errors = True
            error_list.append(db_service_code_master.PASSWORD_INVALID_LENGTH)
        # check password strength
        elif not db_helper_functions.validate_password(password_input):
            contains_errors = True
            error_list.append(db_service_code_master.PASSWORD_INVALID_SYNTAX)
        elif not contains_errors:
            output_dict.update(
                {'password': db_helper_functions.password_encrypt(password_input)})

    if email_input != None:
        if len(email_input) > 255 or len(email_input) <= 0:
            contains_errors = True
            error_list.append(db_service_code_master.EMAIL_INVALID_LENGTH)
        # match email regex
        elif not db_helper_functions.validate_email(email_input):
            contains_errors = True
            error_list.append(db_service_code_master.EMAIL_INVALID_SYNTAX)
        elif not contains_errors:
            output_dict.update(
                {'email': db_helper_functions.string_sanitise(email_input)})

    if phone_no_input != None:
        # match phone regex
        if not db_helper_functions.validate_phone_no(phone_no_input):
            contains_errors = True
            error_list.append(db_service_code_master.PHONE_NUMBER_INVALID)
        elif not contains_errors:
            output_dict.update({'phone_no': phone_no_input})

    if full_name_input != None:
        if len(full_name_input) > 255 or len(full_name_input) <= 0:
            contains_errors = True
            error_list.append(db_service_code_master.FULL_NAME_INVALID_LENGTH)
        elif not contains_errors:
            output_dict.update(
                {'full_name': db_helper_functions.string_sanitise(full_name_input)})

    if contains_errors:
        return {'result': db_service_code_master.USER_INFO_INVALID,
                'reason': error_list}

    return {'result': db_service_code_master.USER_INFO_VALID,
            'content': output_dict}


def login_user(email_input, password_input):
    """
    Takes an input email and password and verifies that it exists in the database.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, LOGIN_FAILURE or LOGIN_SUCCESS.\n
    <reason> (if <result> is LOGIN_FAILURE) [Array] Reason for failure.
    \t[EMAIL_PASSWORD_INVALID]
    """

    # 1.1: email > check[length]
    if len(email_input) > 255:
        return {'result': db_service_code_master.LOGIN_FAILURE,
                'reason': [db_service_code_master.EMAIL_PASSWORD_INVALID]}
    # 1.2: email > check[syntax]
    if not db_helper_functions.validate_email(email_input):
        return {'result': db_service_code_master.LOGIN_FAILURE,
                'reason': [db_service_code_master.EMAIL_PASSWORD_INVALID]}
    # 1.3: sanitise email
    email_sanitised = db_helper_functions.string_sanitise(email_input)

    # 2.1: get first row of email, if any.
    user_info_dict_out = get_user_info_dict(column_names=['password'],
                                            where_array=[['email', email_sanitised]])
    # check if error
    if user_info_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return user_info_dict_out
    # check if empty
    if user_info_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.LOGIN_FAILURE,
                'reason': [db_service_code_master.EMAIL_PASSWORD_INVALID]}
    # 2.2: obtain account password hash
    password_hash_string = user_info_dict_out['content'][0]['password']
    # 2.3: check if passwords match
    if db_helper_functions.password_check(password_input, password_hash_string):
        return {'result': db_service_code_master.LOGIN_SUCCESS}
    else:
        return {'result': db_service_code_master.LOGIN_FAILURE,
                'reason': [db_service_code_master.EMAIL_PASSWORD_INVALID]}


def get_user_id_by_email(email_input):
    """
    Takes an input email and verifies that it exists in the database.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, ACCOUNT_NOT_FOUND or ACCOUNT_FOUND.\n
    <content> (if <result> is ACCOUNT_FOUND) =Value= containing user_id.
    """

    # sanitise email
    email_sanitised = db_helper_functions.string_sanitise(email_input)

    # get user_id from email
    user_info_dict_out = get_user_info_dict(column_names=['id'],
                                            where_array=[['email', email_sanitised]])
    # check if error
    if user_info_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return user_info_dict_out
    # check if empty
    if user_info_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.ACCOUNT_NOT_FOUND}

    return {"result": db_service_code_master.ACCOUNT_FOUND,
            "content": user_info_dict_out['content'][0]['id']}
