import datetime
import helper_functions
import db_methods

# This feels very much like C, how do i make that not so?
ACCOUNT_ALREADY_EXISTS = 1
USERNAME_INVALID_LENGTH = 2
PASSWORD_INVALID_LENGTH = 3
PASSWORD_INVALID_SYNTAX = 4
EMAIL_INVALID_LENGTH = 5
EMAIL_INVALID_SYNTAX = 6
PHONE_NUMBER_INVALID = 7
FULL_NAME_INVALID_LENGTH = 8

CREATE_SUCCESS = 100
LOGIN_SUCCESS = 101
LOGIN_FAILURE = 102

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
    LOGIN_SUCCESS: "Login Successful!",
    LOGIN_FAILURE: "Email or Password is incorrect."
}


def create_user(input_username, input_password, input_email, input_full_name, input_phone_no):
    """
    INSERTS a new user into database.
    Returns an integer, >0 means failure. Check service_code_dict for mappings.
    TODO far in future: return a list of errors instead of just first error encountered.
    id: guid
    username: varchar(64)
    password: varchar(64) [>=8 chars, at least: 1upper, 1lower, 1number]
    email: varchar(255)
    full_name: varchar(255)
    phone_no: integer(8) {nullable}
    created_at: datetime
    modified_at: datetime
    """
    # check provided fields for compliance

    # input_username > check[length]
    if len(input_username) > 64:
        return USERNAME_INVALID_LENGTH
    username = helper_functions.string_sanitise(input_username)

    # password > check[length, security level]
    if len(input_password) > 64:
        return PASSWORD_INVALID_LENGTH
    if not helper_functions.validate_password(input_password):
        return PASSWORD_INVALID_SYNTAX
    hashed_password = helper_functions.password_encrypt(input_password)

    # email > check[length, syntax, already exists]
    if len(input_email) > 255:
        return EMAIL_INVALID_LENGTH
    if not helper_functions.validate_email(input_email):
        return EMAIL_INVALID_SYNTAX
    email = helper_functions.string_sanitise(input_email)
    if db_methods.check_if_exists("user_info", "email", email):
        return ACCOUNT_ALREADY_EXISTS

    # phone_no > check[length, syntax]
    if not helper_functions.validate_phone_no(input_phone_no):
        return PHONE_NUMBER_INVALID
    phone_no = input_phone_no

    # full_name > check[length]
    if len(input_full_name) > 255:
        return FULL_NAME_INVALID_LENGTH
    full_name = helper_functions.string_sanitise(input_full_name)

    # previous checks passed, generate rest of the fields
    id = helper_functions.generate_uuid()
    created_at = datetime.datetime.now()
    modified_at = datetime.datetime.now()

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    task = (id, username, hashed_password, email,
            full_name, phone_no, created_at, modified_at)
    cursor.execute('INSERT INTO user_info VALUES (?,?,?,?,?,?,?,?)', task)

    conn.commit()
    db_methods.close_connection(conn)

    return CREATE_SUCCESS


def login_user(input_email, input_password):
    """
    Takes an input email and password and verifies that it exists in the database.
    Returns an integer, >0 means failure. Check service_code_dict for mappings.
    TODO far in future: return a list of errors instead of just first error encountered.
    """

    # validate email
    if len(input_email) > 255:
        return EMAIL_INVALID_LENGTH
    if not helper_functions.validate_email(input_email):
        return EMAIL_INVALID_SYNTAX
    email = helper_functions.string_sanitise(input_email)

    # get first row of email, if any
    row = db_methods.get_first_row(
        table_name="user_info", columns="password", where_column_name="email", sanitised_value=email)

    if row is None:
        return LOGIN_FAILURE

    password_hash_string = row[0]

    if helper_functions.password_check(input_password, password_hash_string):
        return LOGIN_SUCCESS
    else:
        return LOGIN_FAILURE


