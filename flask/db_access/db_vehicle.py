import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods

import db_access.db_user_info as db_user_info
import db_access.db_connector_type as db_connector_type


def add_vehicle(input_email, input_vehicle_name, input_vehicle_model, input_vehicle_sn, input_vehicle_connector):
    """
    Attempts to insert a new vehicle into the database.\n
    Returns Dictionary with keys:\n
    <result> VEHICLE_ADD_FAILURE or VEHICLE_ADD_SUCCESS.\n
    <reason> (if <result> is VEHICLE_ADD_FAILURE) [Array] Reason for failure.
    \t[reasons]:\n
    \t[VEHICLE_NAME_INVALID_LENGTH, VEHICLE_MODEL_INVALID_LENGTH, VEHICLE_SN_INVALID_LENGTH, CONNECTOR_NOT_FOUND]
    """

    contains_errors = False
    error_list = []

    # 1.1: check if email exists
    user_response = db_user_info.get_user_id_by_email(input_email=input_email)
    if user_response['result'] == db_service_code_master.ACCOUNT_NOT_FOUND:
        contains_errors = True
        error_list.append(user_response['result'])
    # 1.2: store user id
    else:
        user_id = user_response['content']

    # 2.1: input_vehicle_name > check[length]
    if len(input_vehicle_name) > 64 or len(input_vehicle_name) == 0:
        contains_errors = True
        error_list.append(db_service_code_master.VEHICLE_NAME_INVALID_LENGTH)
    # 2.2: sanitise and store vehicle name
    else:
        vehicle_name = db_helper_functions.string_sanitise(input_vehicle_name)

    # 3.1: input_vehicle_model > check[length]
    if len(input_vehicle_model) > 64 or len(input_vehicle_model) == 0:
        contains_errors = True
        error_list.append(db_service_code_master.VEHICLE_MODEL_INVALID_LENGTH)
    # 3.2: sanitise and store vehicle model
    else:
        vehicle_model = db_helper_functions.string_sanitise(input_vehicle_model)

    # 4.1: input_vehicle_sn > check[length]
    if len(input_vehicle_sn) > 8 or len(input_vehicle_sn) == 0:
        contains_errors = True
        error_list.append(db_service_code_master.VEHICLE_SN_INVALID_LENGTH)
    # 4.2: sanitise and storel vehicle SN
    else:
        vehicle_sn = db_helper_functions.string_sanitise(input_vehicle_sn)

    # 5.1: check if connector exists
    connector_response = db_connector_type.get_connector_id_by_name_short(
        input_vehicle_connector)
    if connector_response['result'] == db_service_code_master.CONNECTOR_NOT_FOUND:
        contains_errors = True
        error_list.append(connector_response['result'])
    # 5.2: store connector id
    else:
        connector_id = connector_response['content']

    if contains_errors:
        return {'result': db_service_code_master.VEHICLE_ADD_FAILURE, 'reason': error_list}

    # 6: insert new vehicle
    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    active = True
    task = (db_helper_functions.generate_uuid(), user_id,
            vehicle_name, vehicle_model, vehicle_sn, connector_id, active)
    cursor.execute('INSERT INTO vehicle_info VALUES (?,?,?,?,?,?,?)', task)

    conn.commit()
    db_methods.close_connection(conn)

    return {'result': db_service_code_master.VEHICLE_ADD_SUCCESS}


def get_active_vehicle_by_email(input_email):
    """
    Attempts to get all ACTIVE vehicles for a given user email.\n
    Returns Dictionary with keys:\n
    <result> VEHICLE_NOT_FOUND or VEHICLE_FOUND.\n
    <content> (if <result> is VEHICLE_FOUND) [{Array Dictionary}] containing vehicle information.\n
    \t"keys":\n
    \t{"id", "name", "model", "vehicle_sn", "connector_type"}
    """

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    # sanitise input
    email = db_helper_functions.string_sanitise(input_email)
    task = (email,)
    cursor.execute("""
    SELECT vi.id, vi.name, vi.model, vi.vehicle_sn, ct.name_short AS connector_type FROM vehicle_info AS vi
    LEFT JOIN connector_type AS ct ON vi.id_connector_type = ct.id
    WHERE vi.id_user_info=(SELECT id FROM user_info WHERE email=?) AND vi.active=1
    """, task)

    rows = cursor.fetchall()
    db_methods.close_connection(conn)

    if db_methods.check_fetchall_has_nothing(rows):
        return {'result': db_service_code_master.VEHICLE_NOT_FOUND}

    key_values = []
    # transforming array to key-values
    for row in rows:
        key_values.append({"id": row[0], "name": row[1], "model": row[2],
                          "vehicle_sn": row[3], "connector_type": row[4]})

    return {'result': db_service_code_master.VEHICLE_FOUND,
            'content': key_values}

def remove_vehicle(input_vehicle_id):
    """
    Attempts to set a specific vehicle's active state to false.\n
    Returns Dictionary with keys:\n
    <result> VEHICLE_REMOVE_FAILURE or VEHICLE_REMOVE_SUCCESS.\n
    <reason> (if <result> is VEHICLE_REMOVE_FAILURE) [Array] Reason for failure.
    \t[reasons]:\n
    \t[VEHICLE_NOT_FOUND]
    """

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    # sanitise input
    vehicle_id = db_helper_functions.string_sanitise(input_vehicle_id)
    task = (vehicle_id,)
    cursor.execute('UPDATE vehicle_info SET active=false WHERE id=?', task)
    conn.commit()
    
    cursor.execute('SELECT changes()')

    rows = cursor.fetchone()
    db_methods.close_connection(conn)

    if rows[0] != 1:
        return {'result': db_service_code_master.VEHICLE_REMOVE_FAILURE, 'reason': [db_service_code_master.VEHICLE_NOT_FOUND]}

    return {'result': db_service_code_master.VEHICLE_REMOVE_SUCCESS}