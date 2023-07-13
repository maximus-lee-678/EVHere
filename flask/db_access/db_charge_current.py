# Universal imports
import copy
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods
import db_access.db_universal as db_universal

# Other db_access imports
#

# Generics
column_sql_translations = {'id': 'id', 'id_charge_history': 'id_charge_history',
                           'percentage_current': 'percentage_current', 'last_updated': 'last_updated'}
column_names_all = ['id', 'id_charge_history',
                    'percentage_current', 'last_updated']
trailing_query = """
FROM charge_current
"""


def get_charge_current_hash_map(column_names=None, where_array=None):
    """
    \tcolumn_names >> any combination of ['id', 'id_charge_history', 'percentage_current', 'last_updated']\n
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


def get_charge_current_dict(
    column_names=['id', 'id_charge_history',
                  'percentage_current', 'last_updated'],
    where_array=None
):
    """
    \tcolumn_names >> any combination of ['id', 'id_charge_history', 'percentage_current', 'last_updated']\n
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


def add_charge_current(id_charge_history, percentage_current):
    """
    Inserts a charge current entry into the database. This function assumes input is legal, as it cannot be called directly.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR or CHARGE_CURRENT_CREATE_SUCCESS.
    """

    # generate rest of the fields
    id = db_helper_functions.generate_uuid()
    last_updated = db_helper_functions.generate_time_now()

    query = 'INSERT INTO charge_current VALUES (?,?,?,?)'
    task = (id, id_charge_history, percentage_current, last_updated)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.CHARGE_CURRENT_CREATE_SUCCESS}


def update_charge_current(id_charge_history, percentage_current):
    pass


def remove_charge_current(id_charge_history):
    """
    Removes a charge current entry from the database. This function assumes input is legal, as it cannot be called directly.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR or CHARGE_CURRENT_REMOVE_SUCCESS.
    """
    query = 'DELETE FROM charge_current WHERE id_charge_history=?'
    task = (id_charge_history,)

    transaction = db_methods.safe_transaction(query=query, task=task)
    if not transaction['transaction_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}

    return {'result': db_service_code_master.CHARGE_CURRENT_REMOVE_SUCCESS}
