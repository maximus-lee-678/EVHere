import helper_functions

import db_methods
import db_user_info
import db_connector_type

VEHICLE_NAME_INVALID_LENGTH = 1
VEHICLE_MODEL_INVALID_LENGTH = 2
VEHICLE_SN_INVALID_LENGTH = 3

ADD_SUCCESS = 100
REMOVE_SUCCESS = 101
ADD_FAILURE = 102
REMOVE_FAILURE = 103
BAD_EMAIL = 104
BAD_CONNECTOR = 105
VEHICLE_FOUND = 106
VEHICLE_NOT_FOUND = 107

service_code_dict = {
    VEHICLE_NAME_INVALID_LENGTH: "Name field contains string of invalid length.",
    VEHICLE_MODEL_INVALID_LENGTH: "Model field contains string of invalid length.",
    VEHICLE_SN_INVALID_LENGTH: "Serial Number field contains string of invalid length.",
    ADD_SUCCESS: "Vehicle added.",
    REMOVE_SUCCESS: "Vehicle removed.",
    ADD_FAILURE: "Vehicle could not be added.",
    REMOVE_FAILURE: "Vehicle could not be removed.",
    BAD_EMAIL: "Email not valid.",
    BAD_CONNECTOR: "Connector not valid.",
    VEHICLE_FOUND: "Found vehicles.",
    VEHICLE_NOT_FOUND: "No vehicles were found."
}


def add_vehicle(input_email, input_vehicle_name, input_vehicle_model, input_vehicle_sn, input_vehicle_connector):
    """
    Attempts to insert a new vehicle into the database.\n
    Returns Dictionary with keys:\n
    <result> ADD_FAILURE or ADD_SUCCESS.\n
    <reason> (if <result> is ADD_FAILURE) Reason for failure. (IN ARRAY FORMAT)
    """

    contains_errors = False
    error_list = []

    # 1.1: check if email exists
    user_response = db_user_info.get_user_id_by_email(input_email=input_email)
    if user_response['result'] == db_user_info.ACCOUNT_NOT_FOUND:
        contains_errors = True
        error_list.append(BAD_EMAIL)
    # 1.2: store user id
    else:
        user_id = user_response['content']

    # 2.1: input_vehicle_name > check[length]
    if len(input_vehicle_name) > 64 or len(input_vehicle_name) == 0:
        contains_errors = True
        error_list.append(VEHICLE_NAME_INVALID_LENGTH)
    # 2.2: sanitise and store vehicle name
    else:
        vehicle_name = helper_functions.string_sanitise(input_vehicle_name)

    # 3.1: input_vehicle_model > check[length]
    if len(input_vehicle_model) > 64 or len(input_vehicle_model) == 0:
        contains_errors = True
        error_list.append(VEHICLE_MODEL_INVALID_LENGTH)
    # 3.2: sanitise and store vehicle model
    else:
        vehicle_model = helper_functions.string_sanitise(input_vehicle_model)

    # 4.1: input_vehicle_sn > check[length]
    if len(input_vehicle_sn) > 8 or len(input_vehicle_sn) == 0:
        contains_errors = True
        error_list.append(VEHICLE_SN_INVALID_LENGTH)
    # 4.2: sanitise and storel vehicle SN
    else:
        vehicle_sn = helper_functions.string_sanitise(input_vehicle_sn)

    # 5.1: check if connector exists
    connector_response = db_connector_type.get_connector_id_by_name_short(
        input_vehicle_connector)
    if connector_response['result'] == db_connector_type.CONNECTOR_NOT_FOUND:
        contains_errors = True
        error_list.append(BAD_CONNECTOR)
    # 5.2: store connector id
    else:
        connector_id = connector_response['content']

    if contains_errors:
        return {'result': ADD_FAILURE, 'reason': error_list}

    # 6: insert new vehicle
    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    active = True
    task = (helper_functions.generate_uuid(), user_id,
            vehicle_name, vehicle_model, vehicle_sn, connector_id, active)
    cursor.execute('INSERT INTO vehicle_info VALUES (?,?,?,?,?,?,?)', task)

    conn.commit()
    db_methods.close_connection(conn)

    return {'result': ADD_SUCCESS}


def get_active_vehicle_by_email(input_email):
    """
    Attempts to get all ACTIVE vehicles for a given user email.\n
    Returns Dictionary with keys:\n
    <result> VEHICLE_NOT_FOUND or VEHICLE_FOUND.\n
    <reason> (if <result> is VEHICLE_FOUND) Dictionary containing vehicle information.
    """

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    # sanitise input
    email = helper_functions.string_sanitise(input_email)
    task = (email,)
    cursor.execute("""
    SELECT vi.id, vi.name, vi.model, vi.vehicle_sn, ct.name_short AS connector_type FROM vehicle_info AS vi
    LEFT JOIN connector_type AS ct ON vi.id_connector_type = ct.id
    WHERE vi.id_user_info=(SELECT id FROM user_info WHERE email=?) AND vi.active=1
    """, task)

    rows = cursor.fetchall()
    db_methods.close_connection(conn)

    if db_methods.check_fetchall_has_nothing(rows):
        return {'result': VEHICLE_NOT_FOUND}

    key_values = []
    # transforming array to key-values
    for row in rows:
        key_values.append({"id": row[0], "name": row[1], "model": row[2],
                          "vehicle_sn": row[3], "connector_type": row[4]})

    return {'result': VEHICLE_FOUND,
            'content': key_values}

def remove_vehicle(input_vehicle_id):
    """
    Attempts to set a specific vehicle's active state to false.\n
    Returns Dictionary with keys:\n
    <result> VEHICLE_NOT_FOUND or VEHICLE_FOUND.\n
    <reason> (if <result> is VEHICLE_FOUND) Dictionary containing vehicle information.
    """

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    # sanitise input
    vehicle_id = helper_functions.string_sanitise(input_vehicle_id)
    task = (vehicle_id,)
    cursor.execute('UPDATE vehicle_info SET active=false WHERE id=?', task)
    conn.commit()
    
    cursor.execute('SELECT changes()')

    rows = cursor.fetchone()
    db_methods.close_connection(conn)

    if rows[0] != 1:
        return {'result': REMOVE_FAILURE, 'reason': VEHICLE_NOT_FOUND}

    return {'result': REMOVE_SUCCESS}