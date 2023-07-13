import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods


def get_universal_hash_map(column_names, column_sql_translations, trailing_query, where_array):
    """
    =INTERNAL HELPER METHOD=\n
    Retrieves chosen rows of a table, loads into hashmap with id being the key, and other fields being the value.\n
    This is used to separate retrieval concerns, although joins are still performed by the parent method.\n
    \tcolumn_names >> [Array with key strings]\n
    \tcolumn_sql_translations >> {Dictionary} with mappings\n
    \ttrailing_query >> the rest of the damn query\n
    \twhere_array >> an [Array] containing more [Arrays][2], [Array][0] being WHERE column and [Array][1] being WHERE value e.g. [['id', '0'], ['id', '1']]
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, HASHMAP_GENERIC_EMPTY or HASHMAP_GENERIC_SUCCESS.\n
    <content> (if <result> is HASHMAP_GENERIC_SUCCESS) {Dictionary} containing table information.\n
    \t{"id": {...more key-values...}}
    """

    # select clause: joins values of column_sql_translations if the value's key is found in column_names
    query = f"""
    SELECT {column_sql_translations['id']}, {', '.join(column_sql_translations[column] for column in column_names if column in column_sql_translations)}
    {trailing_query}
    {'' if where_array is None else 
    'WHERE ' + ' AND '.join(f'{column_sql_translations[item[0]]}=?'
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


def get_universal_dict(column_names, column_sql_translations, trailing_query, where_array):
    """
    =INTERNAL HELPER METHOD=\n
    Retrieves chosen rows of a table, loads into dictionary.\n
    This is used to separate retrieval concerns, although joins are still performed by the parent method.\n
    \tcolumn_names >> [Array with key strings]\n
    \tcolumn_sql_translations >> {Dictionary} with mappings\n
    \ttrailing_query >> the rest of the damn query\n
    \twhere_array >> an [Array] containing more [Arrays][2], [Array][0] being WHERE column and [Array][1] being WHERE value e.g. [['id', '0'], ['id', '1']]
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, SELECT_GENERIC_EMPTY or SELECT_GENERIC_SUCCESS.\n
    <content> (if <result> is SELECT_GENERIC_SUCCESS) {Dictionary} containing table information.\n
    \t{...key-values...}
    """

    # select clause: joins values of column_sql_translations if the value's key is found in column_names
    # where clause: joins values of where_array if the value's key is found in column_names, item[0] being
    # column_sql_translations key's associated value, item[1] being actual value
    query = f"""
    SELECT {', '.join(column_sql_translations[column] for column in column_names if column in column_sql_translations)}
    {trailing_query}
    {'' if where_array is None else 
    'WHERE ' + ' AND '.join(f'{column_sql_translations[item[0]]}=?'
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
    =INTERNAL HELPER METHOD=\n
    Takes an output from get_universal_hash_map or get_universal_dict and
    swaps the result key's value with a more specific one specified by operation_type.\n
    No return because dictionaries are pass by reference.
    """
    try:
        input.update({'result': db_service_code_master.translations[input['result']][operation_type]})
    except KeyError as ke:
        pass