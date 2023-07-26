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
    | **[SUPPORTING]**
    | **User Info Hashmap supported fields:** 
    | ['id', 'username', 'password', 'email', 'full_name', 'phone_no', 'created_at', 'modified_at']

    :param array column_names: any combination of supported fields
    :param array where_array: containing more arrays[2-3], array[0] being WHERE column, array[1] being WHERE value, array[2] optionally being 'NOT' e.g. [['id', '0'], ['id', '1', 'NOT]]

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, HASHMAP_GENERIC_EMPTY, HASHMAP_GENERIC_SUCCESS. 
    :key 'content': (dictionary) *('result' == HASHMAP_GENERIC_SUCCESS)* Output. ('id' as key)
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    return db_universal.get_universal_hash_map(column_names=column_names,
                                               column_sql_translations=column_sql_translations,
                                               trailing_query=trailing_query,
                                               where_array=where_array)


def get_user_info_dict(column_names=None, where_array=None):
    """
    | **[SUPPORTING]**
    | **User Info Dictionary supported fields:** 
    | ['id', 'username', 'password', 'email', 'full_name', 'phone_no', 'created_at', 'modified_at']

    :param array column_names: any combination of supported fields
    :param array where_array: containing more arrays[2-3], array[0] being WHERE column, array[1] being WHERE value, array[2] optionally being 'NOT' e.g. [['id', '0'], ['id', '1', 'NOT]]

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, SELECT_GENERIC_EMPTY, SELECT_GENERIC_SUCCESS. 
    :key 'content': (dictionary array) *('result' == SELECT_GENERIC_SUCCESS)* Output.
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    return db_universal.get_universal_dict(column_names=column_names,
                                           column_sql_translations=column_sql_translations,
                                           trailing_query=trailing_query,
                                           where_array=where_array)


def create_user(username_input, password_input, email_input, full_name_input, phone_no_input):
    """
    | **[ENDPOINT]**
    | Attempts to insert a new user into the database.

    :param string username_input: username_input
    :param string password_input: password_input
    :param string email_input: email_input
    :param string full_name_input: full_name_input
    :param string phone_no_input: phone_no_input

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, USER_INFO_CREATE_FAILURE, USER_INFO_CREATE_SUCCESS. 
    :key 'reason': (array, one/multiple) *('result' == USER_INFO_CREATE_FAILURE)* USERNAME_INVALID_LENGTH, PASSWORD_INVALID_LENGTH, PASSWORD_INVALID_SYNTAX, EMAIL_INVALID_LENGTH, EMAIL_INVALID_SYNTAX, ACCOUNT_ALREADY_EXISTS, PHONE_NUMBER_INVALID, FULL_NAME_INVALID_LENGTH
    """

    contains_errors = False
    error_list = []

    user_info_out = validate_user_info(username_input=username_input,
                                       password_input=password_input,
                                       email_input=email_input,
                                       full_name_input=full_name_input,
                                       phone_no_input=phone_no_input)

    if user_info_out['result'] == db_service_code_master.USER_INFO_INVALID:
        contains_errors = True
        error_list = user_info_out['reason']
    else:
        # check for email duplicate
        user_info_dict_out = get_user_info_dict(column_names=['id'],
                                                where_array=[['email', user_info_out['content']['email']]])
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
    task = (id, user_info_out['content']['username'], user_info_out['content']['password'], user_info_out['content']['email'],
            user_info_out['content']['full_name'], user_info_out['content']['phone_no'], created_at, modified_at)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.USER_INFO_CREATE_SUCCESS}


def get_user_info_by_user_id(id_user_info_sanitised):
    """
    | **[ENDPOINT]**
    | Retrieves a user's details.
    | **Fields returned:** {'username', 'email', 'full_name', 'phone_no', 'created_at', 'modified_at'}

    :param string id_user_info_sanitised: id_user_info_sanitised

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, ACCOUNT_NOT_FOUND, ACCOUNT_FOUND. 
    :key 'content': (dictionary) *('result' == ACCOUNT_FOUND)* Output.
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
    | **[ENDPOINT]**
    | Updates a user's details.

    :param string username_input: username_input
    :param string password_input: password_input
    :param string email_input: email_input
    :param string full_name_input: full_name_input
    :param string phone_no_input: phone_no_input

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, USER_INFO_UPDATE_FAILURE, USER_INFO_UPDATE_SUCCESS. 
    :key 'reason': (array, one/multiple) *('result' == USER_INFO_UPDATE_FAILURE)* USERNAME_INVALID_LENGTH, PASSWORD_INVALID_LENGTH, PASSWORD_INVALID_SYNTAX, EMAIL_INVALID_LENGTH, EMAIL_INVALID_SYNTAX, ACCOUNT_ALREADY_EXISTS, PHONE_NUMBER_INVALID, FULL_NAME_INVALID_LENGTH, ACCOUNT_NOT_FOUND
    :key 'content': (string) *('result' == USER_INFO_UPDATE_SUCCESS)* Sanitised email string.
    """

    contains_errors = False
    error_list = []

    user_info_out = validate_user_info(username_input=username_input,
                                       password_input=password_input,
                                       email_input=email_input,
                                       full_name_input=full_name_input,
                                       phone_no_input=phone_no_input)

    if user_info_out['result'] == db_service_code_master.USER_INFO_INVALID:
        contains_errors = True
        error_list = user_info_out['reason']
    else:
        # check for email duplicate, but ignore if self
        user_info_dict_out = get_user_info_dict(column_names=['id'],
                                                where_array=[['email', user_info_out['content']['email']], ['id', id_user_info_sanitised, 'NOT']])
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

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if transaction['rows_affected'] != 1:
        return {'result': db_service_code_master.USER_INFO_UPDATE_FAILURE, 'reason': [db_service_code_master.ACCOUNT_NOT_FOUND]}

    return {'result': db_service_code_master.USER_INFO_UPDATE_SUCCESS, 'content': user_info_out['content']['email']}


def validate_user_info(username_input=None, password_input=None, email_input=None, full_name_input=None, phone_no_input=None):
    """
    | **[INTERNAL]**
    | Takes inputs bound for insertion into 'user info' table and validates it. If valid, also sanitises and hashes where needed.
    | **Fields returned:** {'username', 'email', 'full_name', 'phone_no'} (returns only what it is provided with)

    :param string username_input: username_input (can be None)
    :param string password_input: password_input (can be None)
    :param string email_input: email_input (can be None)
    :param string full_name_input: full_name_input (can be None)
    :param string phone_no_input: phone_no_input (can be None)

    :returns: Dictionary
    :key 'result': (one) USER_INFO_INVALID, USER_INFO_VALID. 
    :key 'reason': (array, one/multiple) *('result' == USER_INFO_INVALID)* USERNAME_INVALID_LENGTH, PASSWORD_INVALID_LENGTH, PASSWORD_INVALID_SYNTAX, EMAIL_INVALID_LENGTH, EMAIL_INVALID_SYNTAX, ACCOUNT_ALREADY_EXISTS, PHONE_NUMBER_INVALID, FULL_NAME_INVALID_LENGTH
    :key 'content': (dictionary) *('result' == USER_INFO_UPDATE_SUCCESS)* Output.
    """

    contains_errors = False
    error_list = []
    output_dict = {}

    if username_input != None:
        if len(username_input) > 64 or len(username_input) <= 0:
            contains_errors = True
            error_list.append(db_service_code_master.USERNAME_INVALID_LENGTH)
        elif not contains_errors:
            output_dict.update({'username': db_helper_functions.string_sanitise(username_input)})

    if password_input != None:
        if len(password_input) > 64 or len(password_input) <= 0:
            contains_errors = True
            error_list.append(db_service_code_master.PASSWORD_INVALID_LENGTH)
        # check password strength
        elif not db_helper_functions.validate_password(password_input):
            contains_errors = True
            error_list.append(db_service_code_master.PASSWORD_INVALID_SYNTAX)
        elif not contains_errors:
            output_dict.update({'password': db_helper_functions.password_encrypt(password_input)})

    if email_input != None:
        if len(email_input) > 255 or len(email_input) <= 0:
            contains_errors = True
            error_list.append(db_service_code_master.EMAIL_INVALID_LENGTH)
        # match email regex
        elif not db_helper_functions.validate_email(email_input):
            contains_errors = True
            error_list.append(db_service_code_master.EMAIL_INVALID_SYNTAX)
        elif not contains_errors:
            output_dict.update({'email': db_helper_functions.string_sanitise(email_input)})

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
            output_dict.update({'full_name': db_helper_functions.string_sanitise(full_name_input)})

    if contains_errors:
        return {'result': db_service_code_master.USER_INFO_INVALID,
                'reason': error_list}

    return {'result': db_service_code_master.USER_INFO_VALID,
            'content': output_dict}


def login_user(email_input, password_input):
    """
    | **[ENDPOINT]**
    | Takes an input email and password and verifies that it exists in the database.

    :param string email_input: email_input
    :param string password_input: password_input

    :returns: Dictionary
    :key 'result': (one) USER_INFO_INVALID, USER_INFO_VALID. 
    :key 'reason': (array, one) *('result' == USER_INFO_INVALID)* EMAIL_PASSWORD_INVALID.
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
    | **[ENDPOINT]**
    | Takes an input email and retrieves the corresponding user id.

    :param string email_input: email_input

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, ACCOUNT_NOT_FOUND, ACCOUNT_FOUND. 
    :key 'content': (string) *('result' == ACCOUNT_FOUND)* user id.
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

    return {'result': db_service_code_master.ACCOUNT_FOUND,
            'content': user_info_dict_out['content'][0]['id']}
