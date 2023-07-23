import sys

import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods


def get_universal_hash_map(column_names=None, column_sql_translations=None, trailing_query=None, where_array=None):
    """
    | **[SUPPORTING]**
    | Simply retrieves chosen rows of a single table, loads into hashmap with id being the key, 
    | other fields containing chosen column key-values. {id: {...}, ...}
    | This is used to separate retrieval concerns. Any joins are performed by the parent method.

    :param array column_names: output key names of chosen column key-values.
    :param dict column_sql_translations: mapping of output key names to SQL column names.
    :param string trailing_query: 'FROM <table_name>'
    :param array where_array: containing more arrays[2-3], array[0] being WHERE column, array[1] being WHERE value, array[2] optionally being 'NOT' e.g. [['id', '0'], ['id', '1', 'NOT]]

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, HASHMAP_GENERIC_EMPTY, HASHMAP_GENERIC_SUCCESS. 
    :key 'content': (dictionary) *('result' == HASHMAP_GENERIC_SUCCESS)* Output. ('id' as key)
    """

    # select clause: joins values of column_sql_translations if the value's key is found in column_names
    # where clause: joins values of where_array if the value's key is found in column_names, item[0] being
    # column_sql_translations key's associated value, item[1] being actual value
    query = f"""
    SELECT {column_sql_translations['id']}, {', '.join(column_sql_translations[column] for column in column_names if column in column_sql_translations)}
    {trailing_query}
    {'' if where_array is None else 
    'WHERE ' + ' AND '.join(f'{item[2] + " " if len(item) == 3 else ""}{column_sql_translations[item[0]]}=?'
                            for item in where_array if item[0] in column_sql_translations.keys())}
    """

    if where_array != None:
        task = tuple(item[1] for item in where_array if item[0] in column_sql_translations.keys())
        select = db_methods.safe_select(query=query, task=task, get_type='all')
    else:
        select = db_methods.safe_select(query=query, task=None, get_type='all')

    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.HASHMAP_GENERIC_EMPTY}

    # first array index is id
    # for rest of array, join column name(key) and rows(value)
    hash_map = {row[0]: dict(zip(column_names, row[1:]))
                for row in select['content']}

    return {'result': db_service_code_master.HASHMAP_GENERIC_SUCCESS, 'content': hash_map}


def get_universal_dict(column_names=None, column_sql_translations=None, trailing_query=None, where_array=None):
    """
    | **[SUPPORTING]**
    | Simply retrieves chosen rows of a single table, loads into dictionary array. [{...}, ...]
    | This is used to separate retrieval concerns. Any joins are performed by the parent method.

    :param array column_names: output key names of chosen column key-values.
    :param dict column_sql_translations: mapping of output key names to SQL column names.
    :param string trailing_query: 'FROM <table_name>'
    :param array where_array: containing more arrays[2-3], array[0] being WHERE column, array[1] being WHERE value, array[2] optionally being 'NOT' e.g. [['id', '0'], ['id', '1', 'NOT]]

    :returns: Dictionary
    :key 'result': (one) INTERNAL_ERROR, SELECT_GENERIC_EMPTY, SELECT_GENERIC_SUCCESS. 
    :key 'content': (dictionary array) *('result' == SELECT_GENERIC_SUCCESS)* Output.
    """

    # select clause: joins values of column_sql_translations if the value's key is found in column_names
    # where clause: joins values of where_array if the value's key is found in column_names, item[0] being
    # column_sql_translations key's associated value, item[1] being actual value
    query = f"""
    SELECT {', '.join(column_sql_translations[column] for column in column_names if column in column_sql_translations)}
    {trailing_query}
    {'' if where_array is None else 
    'WHERE ' + ' AND '.join(f'{item[2] + " " if len(item) == 3 else ""}{column_sql_translations[item[0]]}=?'
                            for item in where_array if item[0] in column_sql_translations.keys())}
    """
    
    if where_array != None:
        task = tuple(item[1] for item in where_array if item[0] in column_sql_translations.keys())
        select = db_methods.safe_select(query=query, task=task, get_type='all')
    else:
        select = db_methods.safe_select(query=query, task=None, get_type='all')

    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.SELECT_GENERIC_EMPTY}

    # join column name(key) and rows(value)
    key_values = [dict(zip(column_names, row))
                  for row in select['content']]

    return {'result': db_service_code_master.SELECT_GENERIC_SUCCESS, 'content': key_values}


def degeneralise_result_codes(input, operation_type):
    """
    | **[INTERNAL]**
    | Takes an output from get_universal_hash_map or get_universal_dict and swaps the result key's value with a more specific one specified by operation_type.
    | No return because dictionaries are pass by reference.

    :param dict input: an output from get_universal_hash_map or get_universal_dict.
    :param int operation_type: a value from db_service_code_master, TYPE_...
    """

    try:
        input.update({'result': db_service_code_master.translations[input['result']][operation_type]})
    except KeyError as ke:
        print('Error when degeneralising result codes: %s' % ke.__class__, file=sys.stderr)
        print('Key is: %s' % input['result'], file=sys.stderr)