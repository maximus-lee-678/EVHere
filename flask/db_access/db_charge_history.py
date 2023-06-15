import db_access.db_helper_functions as db_helper_functions
import db_access.db_methods as db_methods

ACCOUNT_ALREADY_EXISTS = 1
EMAIL_INVALID_LENGTH = 2
EMAIL_INVALID_SYNTAX = 3

service_code_dict = {
    ACCOUNT_ALREADY_EXISTS: "Account already exists in system.",
    EMAIL_INVALID_LENGTH: "Email is of invalid length.",
    EMAIL_INVALID_SYNTAX: "Email is not valid."
}


def add_charge_history_initial(input_email, input_id_vehicle_info, input_id_charger, input_battery_percentage):
    """
    Attempts to insert a charge history into the database. This method will also add an entry to "charge current",
    as this method is called when the user starts a charge.\n
    Returns Dictionary with keys:\n
    <result> CREATE_FAILURE or CREATE_SUCCESS.\n
    <reason> (if <result> is CREATE_FAILURE) Reason for failure. (IN ARRAY FORMAT)
    """

    contains_errors = False
    error_list = []

    # 1.1: email > check[length]
    if len(input_email) > 255 or len(input_email) == 0:
        contains_errors = True
        error_list.append(EMAIL_INVALID_LENGTH)
    # 1.2: email > check[syntax]
    elif not db_helper_functions.validate_email(input_email):
        contains_errors = True
        error_list.append(EMAIL_INVALID_SYNTAX)
    else:
        # 1.3: sanitise email
        email = db_helper_functions.string_sanitise(input_email)
        # 1.4: email > check[already exists]
        conn = db_methods.setup_connection()
        cursor = conn.cursor()
        task = (email,)
        cursor.execute('SELECT * FROM user_info WHERE email=?', task)
        row = cursor.fetchone()
        db_methods.close_connection(conn)
        if not db_methods.check_fetchone_has_nothing(row):
            contains_errors = True
            error_list.append(ACCOUNT_ALREADY_EXISTS)

    