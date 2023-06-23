# Universal imports
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods

# Other db_access imports
import db_access.db_connector_type as db_connector_type


def add_vehicle(id_user_info_sanitised, name_input, model_input, sn_input, connector_input):
    """
    Attempts to insert a new vehicle into the database.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, VEHICLE_ADD_FAILURE or VEHICLE_ADD_SUCCESS.\n
    <reason> (if <result> is VEHICLE_ADD_FAILURE) [Array] Reason for failure.
    \t[reasons]:\n
    \t[VEHICLE_NAME_INVALID_LENGTH, VEHICLE_MODEL_INVALID_LENGTH, VEHICLE_SN_INVALID_LENGTH, CONNECTOR_NOT_FOUND]
    """

    contains_errors = False
    error_list = []

    # 1.1: input_vehicle_name > check[length]
    if len(name_input) > 64 or len(name_input) == 0:
        contains_errors = True
        error_list.append(db_service_code_master.VEHICLE_NAME_INVALID_LENGTH)
    # 1.2: sanitise and store vehicle name
    else:
        name_sanitised = db_helper_functions.string_sanitise(name_input)

    # 2.1: input_vehicle_model > check[length]
    if len(model_input) > 64 or len(model_input) == 0:
        contains_errors = True
        error_list.append(db_service_code_master.VEHICLE_MODEL_INVALID_LENGTH)
    # 2.2: sanitise and store vehicle model
    else:
        model_sanitised = db_helper_functions.string_sanitise(
            model_input)

    # 3.1: input_vehicle_sn > check[length]
    if len(sn_input) > 8 or len(sn_input) == 0:
        contains_errors = True
        error_list.append(db_service_code_master.VEHICLE_SN_INVALID_LENGTH)
    # 3.2: sanitise and store vehicle SN
    else:
        sn_sanitised = db_helper_functions.string_sanitise(sn_input)

    # 4.1: check if connector exists
    connector_response = db_connector_type.get_connector_id_by_name_short(
        connector_input)
    if connector_response['result'] != db_service_code_master.CONNECTOR_FOUND:
        contains_errors = True
        error_list.append(connector_response['result'])
    # 4.2: store connector id
    else:
        connector_id = connector_response['content']

    if contains_errors:
        return {'result': db_service_code_master.VEHICLE_ADD_FAILURE, 'reason': error_list}

    # 5: insert new vehicle
    query = 'INSERT INTO vehicle_info VALUES (?,?,?,?,?,?,?)'
    active = True
    task = (db_helper_functions.generate_uuid(), id_user_info_sanitised,
            name_sanitised, model_sanitised, sn_sanitised, connector_id, active)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.VEHICLE_ADD_SUCCESS}


def remove_vehicle(id_vehicle_input):
    """
    Attempts to set a specific vehicle's active state to false.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, VEHICLE_REMOVE_FAILURE or VEHICLE_REMOVE_SUCCESS.\n
    <reason> (if <result> is VEHICLE_REMOVE_FAILURE) [Array] Reason for failure.
    \t[reasons]:\n
    \t[VEHICLE_NOT_FOUND]
    """

    # sanitise input
    id_vehicle_sanitised = db_helper_functions.string_sanitise(
        id_vehicle_input)

    query = 'UPDATE vehicle_info SET active=false WHERE id=?'
    task = (id_vehicle_sanitised,)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if transaction['rows_affected'] != 1:
        return {'result': db_service_code_master.VEHICLE_REMOVE_FAILURE, 'reason': [db_service_code_master.VEHICLE_NOT_FOUND]}

    return {'result': db_service_code_master.VEHICLE_REMOVE_SUCCESS}


def get_active_vehicle_by_user_id(id_user_info_sanitised):
    """
    Attempts to get all ACTIVE vehicles for a given user id.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, VEHICLE_NOT_FOUND or VEHICLE_FOUND.\n
    <content> (if <result> is VEHICLE_FOUND) [{Array Dictionary}] containing vehicle information.\n
    \t"keys":\n
    \t{"id", "name", "model", "vehicle_sn", "connector_type"}
    """

    query = """
    SELECT vi.id, vi.name, vi.model, vi.vehicle_sn, ct.name_short AS connector_type FROM vehicle_info AS vi
    LEFT JOIN connector_type AS ct ON vi.id_connector_type = ct.id
    WHERE vi.id_user_info=? AND vi.active=1
    """
    task = (id_user_info_sanitised,)

    select = db_methods.safe_select(
        query=query, task=task, get_type='all')
    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.VEHICLE_NOT_FOUND}

    # transforming array to key-values
    key_values = [{"id": row[0], "name": row[1], "model": row[2],
                   "vehicle_sn": row[3], "connector_type": row[4]}
                  for row in select['content']]

    return {'result': db_service_code_master.VEHICLE_FOUND,
            'content': key_values}


def get_vehicle_by_id(id_vehicle_input):
    """
    Attempts to get an ACTIVE vehicle for a given vehicle id.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, VEHICLE_NOT_FOUND or VEHICLE_FOUND.\n
    <content> (if <result> is VEHICLE_FOUND) {Dictionary} containing vehicle information.\n
    \t"keys":\n
    \t{"id", "name", "model", "vehicle_sn", "connector_type"}
    """

    # sanitise input
    vehicle_id_sanitised = db_helper_functions.string_sanitise(
        id_vehicle_input)

    query = """
    SELECT vi.id, vi.name, vi.model, vi.vehicle_sn, ct.name_short AS connector_type FROM vehicle_info AS vi
    LEFT JOIN connector_type AS ct ON vi.id_connector_type = ct.id
    WHERE vi.id=? AND vi.active=1
    """
    task = (vehicle_id_sanitised,)

    select = db_methods.safe_select(
        query=query, task=task, get_type='one')
    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.VEHICLE_NOT_FOUND}

    # transforming row to key-values
    key_values = {"id": select['content'][0], "name": select['content'][1], "model": select['content'][2],
                  "vehicle_sn": select['content'][3], "connector_type": select['content'][4]}

    return {'result': db_service_code_master.VEHICLE_FOUND,
            'content': key_values}
