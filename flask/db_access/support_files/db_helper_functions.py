import re
import uuid
import bcrypt
import datetime


def generate_uuid():
    """
    :returns: (string) random UUID
    """

    return str(uuid.uuid4())


def generate_time_now():
    """
    :returns: (string) current epoch time
    """

    return datetime.datetime.now().isoformat(sep='T', timespec='auto')


def validate_email(email):
    """
    | Used to check if string matches email format

    :param string email: email

    :returns: (bool) True or False
    """

    return re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)


def validate_password(password):
    """
    | Used to check if string fulfils validation criterion: >=8 chars, at least: 1upper, 1lower, 1number

    :param string password: password

    :returns: (bool) True or False
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
    | Used to check if string is an 8 digit phone number

    :param string phone_no: phone_no

    :returns: (bool) True or False
    """

    return re.match(r'^\d{8}$', phone_no)


def validate_currency(currency):
    """
    | Used to check if a string is a number optionally followed by a decimal point and up to 2 digit

    :param string currency: currency

    :returns: (bool) True or False
    """

    return re.match(r'^(\d+(\.\d{1,2})?)$', currency)


def string_sanitise(string):
    """
    | Sanitises string

    :param string string: string

    :returns: (string) sanitised string
    """

    # PHP trim()
    string = string.strip()

    # PHP stripslashes()
    string = string.encode('utf-8').decode('unicode_escape')

    # PHP htmlspecialchars()
    string = string.replace('&', '&amp;').replace('"', '&quot;').replace('\'', '&#039;').replace('<', '&lt;').replace('>', '&gt;')

    return string


def password_encrypt(password):
    """
    | Encrypts string using BCrypt

    :param string password: password

    :returns: (string) hashed string
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
    | Checks if a hash of a string and a hash matches

    :param string password: password
    :param string password_hashed: password_hashed

    :returns: (bool) True or False
    """

    # converting password to array of bytes
    password_bytes = password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, password_hashed)


def update_dict_key(dict=None, key_to_update=None, key_new_name=None, key_new_value=None):
    """
    | Updates a dictionary's key and value.
    | Also usable to add new keys. Leave new_key_name empty.
    | No return because dictionaries are pass by reference.

    :param dict dict: dictionary to update
    :param string key_to_update: name of current key to update
    :param string key_new_name: new key name (optional)
    :param string key_new_value: new value
    """

    # update key value
    dict.update({key_to_update: key_new_value})

    # update key name (if needed)
    if key_new_name != None:
        dict[key_new_name] = dict.pop(key_to_update)


def calculate_charge_cost(energy_drawn, rate):
    """
    | Returns calculated charge cost price to 2 decimal places.
    | No return because dictionaries are pass by reference.

    :param string energy_drawn: energy_drawn
    :param string rate: rate

    :returns: (string) price to 2 decimal places.
    """

    return '{price:.2f}'.format(price=energy_drawn * rate)
