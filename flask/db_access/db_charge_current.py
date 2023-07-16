# Universal imports
import copy
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods
import db_access.db_universal as db_universal

# Other db_access imports
import db_access.db_charger as db_charger
import db_access.db_charger_available_connector as db_charger_available_connector
import db_access.db_charge_history as db_charge_history

# Generics
column_sql_translations = {'id': 'id', 'id_charge_history': 'id_charge_history', 'id_charger_available_connector': 'id_charger_available_connector',
                           'current_energy_drawn': 'current_energy_drawn', 'rate_snapshot': 'rate_snapshot', 'last_updated': 'last_updated'}
column_names_all = ['id', 'id_charge_history', 'id_charger_available_connector',
                    'current_energy_drawn', 'rate_snapshot', 'last_updated']
trailing_query = """
FROM charge_current
"""


def get_charge_current_hash_map(column_names=None, where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'id_charge_history', 'id_charger_available_connector',
                    'current_energy_drawn', 'rate_snapshot', 'last_updated']\n
    \twhere_array >> an [Array] containing more [Arrays][2], [Array][0] being WHERE column and [Array][1] being WHERE value e.g. [['id', '0'], ['id', '1']\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, HASHMAP_GENERIC_EMPTY or HASHMAP_GENERIC_SUCCESS.\n
    <content> (if <result> is HASHMAP_GENERIC_SUCCESS) {Dictionary} containing table information.\n
    \t{"id": {...key-values...}}
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    return db_universal.get_universal_hash_map(column_names=column_names,
                                               column_sql_translations=column_sql_translations,
                                               trailing_query=trailing_query,
                                               where_array=where_array)


def get_charge_current_dict(column_names=None, where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'id_charge_history', 'id_charger_available_connector',
                    'current_energy_drawn', 'rate_snapshot', 'last_updated']\n
    \twhere_array >> an [Array] containing more [Arrays][2], [Array][0] being WHERE column and [Array][1] being WHERE value e.g. [['id', '0'], ['id', '1']\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, SELECT_GENERIC_EMPTY or SELECT_GENERIC_SUCCESS.\n
    <content> (if <result> is SELECT_GENERIC_SUCCESS) {Dictionary} containing table information.\n
    \t{{...key-values...}}
    """

    if column_names == None:
        column_names = copy.deepcopy(column_names_all)

    return db_universal.get_universal_dict(column_names=column_names,
                                           column_sql_translations=column_sql_translations,
                                           trailing_query=trailing_query,
                                           where_array=where_array)


def add_charge_current(id_charge_history, id_charger, id_charger_available_connector_input):
    """
    =CHILD FUNCTION=
    Inserts a charge current entry into the database.\n
    Also toggles charger available connector's 'in use' field.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, AVAILABLE_CONNECTORS_NOT_FOUND, AVAILABLE_CONNECTOR_IN_USE or CHARGE_CURRENT_CREATE_SUCCESS.
    """

    # 1: verify charger available connector exists for given charger and that it is not in use
    charger_dict_out = db_charger.get_charger_dict(column_names=['rate_current', 'available_connector'],
                                                   where_array=[['id', id_charger]])
    if charger_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        return {'result': db_service_code_master.CHARGER_NOT_FOUND}
    if charger_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return charger_dict_out

    charger_available_connectors = charger_dict_out['content'][0]['available_connector']
    connector_found = False
    use_check_failed = False
    id_charger_available_connector_sanitised = db_helper_functions.string_sanitise(
        id_charger_available_connector_input)
    for row in charger_available_connectors:
        if row['id'] == id_charger_available_connector_sanitised:
            connector_found = True
            if row['in_use'] != 0:
                use_check_failed = True
            break

    if not connector_found:
        return {'result': db_service_code_master.AVAILABLE_CONNECTORS_NOT_FOUND}
    if use_check_failed:
        return {'result': db_service_code_master.AVAILABLE_CONNECTOR_IN_USE}

    # 2: capture current price rate of charger
    rate_current = charger_dict_out['content'][0]['rate_current']

    # 3: set charger connector's in_use
    charger_available_connectors_out = db_charger_available_connector.set_charger_available_connector_in_use(
        id_charger_available_connector_sanitised, True)
    if charger_available_connectors_out['result'] != db_service_code_master.AVAILABLE_CONNECTOR_SET_USE_STATE_SUCCESS:
        return {'result': charger_available_connectors_out['result']}

    # generate rest of the fields
    id = db_helper_functions.generate_uuid()
    last_updated = db_helper_functions.generate_time_now()

    query = 'INSERT INTO charge_current VALUES (?,?,?,?,?,?)'
    task = (id, id_charge_history, id_charger_available_connector_sanitised,
            0, rate_current, last_updated)
    
    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.CHARGE_CURRENT_CREATE_SUCCESS}


def update_user_charge_current(id_user_info_sanitised, current_energy_drawn_input):
    """
    TODO replace with periodic automated updates\n
    =CHILD FUNCTION=
    Removes a charge current entry from the database.\n
    Also toggles charger available connector's 'in use' field.\n
    Updates a charge current entry with a new energy drawn value.\n
    <result> INTERNAL_ERROR, CHARGE_CURRENT_UPDATE_FAILURE or CHARGE_CURRENT_UPDATE_SUCCESS.\n
    <reason> (if <result> is CHARGE_CURRENT_UPDATE_FAILURE) [Array] Reason for failure.
    \t[CHARGE_HISTORY_NOT_CHARGING, CHARGER_AVAILABLE_CONNECTOR_INVALID_ENERGY_LEVEL]
    """

    contains_errors = False
    error_list = []

    # 1: check if user is already charging a vehicle
    charge_history_dict_out = db_charge_history.get_charge_history_dict(column_names=['id'],
                                                                        where_array=[['id_user_info', id_user_info_sanitised], ['is_charge_finished', False]])
    if charge_history_dict_out['result'] == db_service_code_master.SELECT_GENERIC_EMPTY:
        contains_errors = True
        error_list.append(
            db_service_code_master.CHARGE_HISTORY_NOT_CHARGING)
    elif charge_history_dict_out['result'] == db_service_code_master.INTERNAL_ERROR:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    else:
        id_charge_history_sanitised = charge_history_dict_out['content'][0]['id']

    # 2: check energy format
    if not current_energy_drawn_input.isdigit():
        contains_errors = True
        error_list.append(
            db_service_code_master.CHARGER_AVAILABLE_CONNECTOR_INVALID_ENERGY_LEVEL)

    if contains_errors:
        return {'result': db_service_code_master.CHARGE_CURRENT_UPDATE_FAILURE,
                'reason': error_list}

    query = 'UPDATE charge_current SET current_energy_drawn=? WHERE id_charge_history=?'
    task = (current_energy_drawn_input, id_charge_history_sanitised)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.CHARGE_CURRENT_UPDATE_SUCCESS}


def remove_charge_current(id_charge_history):
    """
    Removes a charge current entry from the database. This function assumes input is legal, as it cannot be called directly.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR or CHARGE_CURRENT_REMOVE_SUCCESS.
    """

    # get available connector id
    charge_current_dict_out = get_charge_current_dict(column_names=['id_charger_available_connector'],
                                                      where_array=[['id_charge_history', id_charge_history]])
    if charge_current_dict_out['result'] != db_service_code_master.SELECT_GENERIC_SUCCESS:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    id_charger_available_connector = charge_current_dict_out['content'][0]['id_charger_available_connector']

    query = 'DELETE FROM charge_current WHERE id_charge_history=?'
    task = (id_charge_history,)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    
    # set charger connector's in_use
    charger_available_connectors_out = db_charger_available_connector.set_charger_available_connector_in_use(
        id_charger_available_connector, False)
    if charger_available_connectors_out['result'] != db_service_code_master.AVAILABLE_CONNECTOR_SET_USE_STATE_SUCCESS:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.CHARGE_CURRENT_REMOVE_SUCCESS}
