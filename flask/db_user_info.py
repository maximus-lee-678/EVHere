import datetime
import re
import bcrypt
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
    Returns an integer, >0 means failure. Check create_user_code_dict for mappings.
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
    username = string_sanitise(input_username)

    # password > check[length, security level]
    if len(input_password) > 64:
        return PASSWORD_INVALID_LENGTH
    if not validate_password(input_password):
        return PASSWORD_INVALID_SYNTAX
    hashed_password = password_encrypt(input_password)

    # email > check[length, syntax, already exists]
    if len(input_email) > 255:
        return EMAIL_INVALID_LENGTH
    if not validate_email(input_email):
        return EMAIL_INVALID_SYNTAX
    email = string_sanitise(input_email)
    if db_methods.check_if_exists("user_info", "email", email):
        return ACCOUNT_ALREADY_EXISTS

    # phone_no > check[length, syntax]
    if not validate_phone_no(input_phone_no):
        return PHONE_NUMBER_INVALID
    phone_no = input_phone_no

    # full_name > check[length]
    if len(input_full_name) > 255:
        return FULL_NAME_INVALID_LENGTH
    full_name = string_sanitise(input_full_name)

    # previous checks passed, generate rest of the fields
    id = db_methods.generate_uuid()
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
    # validate email
    if len(input_email) > 255:
        return EMAIL_INVALID_LENGTH
    if not validate_email(input_email):
        return EMAIL_INVALID_SYNTAX
    email = string_sanitise(input_email)

    # get first row of email, if any
    row = db_methods.get_first_row(
        table_name="user_info", columns="password", where_column_name="email", sanitised_value=email)

    if row is None:
        return LOGIN_FAILURE

    password_hash_string = row[0]

    if password_check(input_password, password_hash_string):
        return LOGIN_SUCCESS
    else:
        return LOGIN_FAILURE


def validate_email(email):
    """
    Used to check if string matches email format
    """
    return re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)


def validate_password(password):
    """
    Validation criterion: >=8 chars, at least: 1upper, 1lower, 1number
    """
    # Check length
    if len(password) < 8:
        return False

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False

    # Check for at least one number
    if not re.search(r'[0-9]', password):
        return False

    # Check for at least one symbol
    if not re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]', password):
        return False

    # If all conditions pass, return True
    return True


def validate_phone_no(phone_no):
    """
    Checks if string is an 8 digit phone number
    """
    return re.match(r'^\d{8}$', phone_no)


def string_sanitise(string):
    """
    Before storing to database, sanitise and return string
    """
    return string_html_special_chars(string_strip_slashes(string_trim(string)))


def string_trim(string):
    """
    Sanitise phase 1
    """
    return string.strip()


def string_strip_slashes(string):
    """
    Sanitise phase 2
    """
    string = re.sub(r"\\(n|r)", "\n", string)
    string = re.sub(r"\\", "", string)
    return string


def string_html_special_chars(string):
    """
    Sanitise phase 3
    """
    return (
        string
        .replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace('\'', "&#039;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def password_encrypt(password):
    """
    Encrypts and salts the password using BCrypt, returns hash
    """
    # generating the salt
    kripp = bcrypt.gensalt()

    # converting password to array of bytes
    password_bytes = password.encode('utf-8')

    # Hashing the password
    password_hashed = bcrypt.hashpw(password_bytes, kripp)

    return password_hashed


def password_check(password, password_hashed):
    """
    Returns True or False depending on whether 2 hashes match
    """
    # converting password to array of bytes
    password_bytes = password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, password_hashed)
