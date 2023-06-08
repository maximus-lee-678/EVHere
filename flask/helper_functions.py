import re
import uuid
import bcrypt


def generate_uuid():
    """
    Generates random UUID
    """
    return str(uuid.uuid4())


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


def join_strings(service_code_array, service_code_dict):
    """
    Takes an array containing service codes and a service code dictionary and returns a
    space joined string containing decoded service codes.
    """
    service_code_decoded = []
    [service_code_decoded.append(service_code_dict[i])
     for i in service_code_array]

    return ' '.join(service_code_decoded)
