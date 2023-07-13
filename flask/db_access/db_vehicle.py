# Universal imports
import copy
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods
import db_access.db_universal as db_universal

# Other db_access imports
import db_access.db_connector_type as db_connector_type

# Generics:
column_sql_translations = {'id': 'id', 'id_user_info': 'id_user_info', 'name': 'name', 'model': 'model',
                           'vehicle_sn': 'vehicle_sn', 'connector': 'id_connector_type', 'active': 'active'}
column_names_all = ['id', 'id_user_info', 'name',
                    'model', 'vehicle_sn', 'connector', 'active']
trailing_query = """
FROM vehicle_info
"""


def get_vehicle_hash_map(column_names=None, where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'id_user_info', 'name', 'model', 'vehicle_sn', 'connector', 'active']\n
    \twhere_array >> an [Array] containing more [Arrays][2], [Array][0] being WHERE column and [Array][1] being WHERE value e.g. [['id', '0'], ['id', '1']\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, HASHMAP_GENERIC_EMPTY or HASHMAP_GENERIC_SUCCESS.\n
    <content> (if <result> is HASHMAP_GENERIC_SUCCESS) {Dictionary} containing table information.\n
    \t{"id": {...key-values...}}
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    vehicle_hash_map_out = db_universal.get_universal_hash_map(column_names=column_names,
                                               column_sql_translations=column_sql_translations,
                                               trailing_query=trailing_query,
                                               where_array=where_array)
    
    if 'connector' in column_names:
        connector_type_hash_map_out = db_connector_type.get_connector_type_hash_map()

        for value in vehicle_hash_map_out['content'].values():
            db_helper_functions.update_dict_key(
                dict=value, key_to_update='connector', new_key_name=None, new_key_value=connector_type_hash_map_out['content'][value['connector']])
    
    return vehicle_hash_map_out


def get_vehicle_dict(column_names=None, where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'id_user_info', 'name', 'model', 'vehicle_sn', 'connector', 'active']\n
    \twhere_array >> an [Array] containing more [Arrays][2], [Array][0] being WHERE column and [Array][1] being WHERE value e.g. [['id', '0'], ['id', '1']\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, SELECT_GENERIC_EMPTY or SELECT_GENERIC_SUCCESS.\n
    <content> (if <result> is SELECT_GENERIC_SUCCESS) {Dictionary} containing table information.\n
    \t{{...key-values...}}
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    vehicle_dict_out = db_universal.get_universal_dict(column_names=column_names,
                                                       column_sql_translations=column_sql_translations,
                                                       trailing_query=trailing_query,
                                                       where_array=where_array)

    if 'connector' in column_names:
        connector_type_hash_map_out = db_connector_type.get_connector_type_hash_map()

        for row in vehicle_dict_out['content']:
            db_helper_functions.update_dict_key(
                dict=row, key_to_update='connector', new_key_name=None, new_key_value=connector_type_hash_map_out['content'][row['connector']])

    return vehicle_dict_out


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
    connector_type_dict_out = db_connector_type.get_connector_type_dict(column_names=['id'],
                                                                        where_array=[['id', connector_input]])
    # check if empty or error
    if connector_type_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        contains_errors = True
        error_list.append(db_service_code_master.CONNECTOR_NOT_FOUND)
    elif connector_type_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        contains_errors = True
        error_list.append(connector_type_dict_out['result'])
    # 4.2: store connector id (sanitised)
    else:
        connector_id = connector_type_dict_out['content'][0]['id']

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

    vehicle_dict_out = get_vehicle_dict(column_names=['id', 'name', 'model', 'vehicle_sn', 'connector'],
                                        where_array=[['id_user_info', id_user_info_sanitised], ['active', '1']])
    # check if empty or error
    if vehicle_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.VEHICLE_NOT_FOUND}
    if vehicle_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return vehicle_dict_out

    return {'result': db_service_code_master.VEHICLE_FOUND,
            'content': vehicle_dict_out['content']}
