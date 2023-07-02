import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods


def get_all_universal_hash_map(column_names, column_sql_translations, trailing_query):
    """
    =INTERNAL HELPER METHOD=\n
    Retrieves ALL rows of a table, loads into hashmap with id being the key, and other fields being the value.\n
    This is used to separat retrieval concerns, although joins are still performed by the parent method.\n
    \tcolumn_names >> [Array with key strings]\n
    \tcolumn_sql_translations >> {Dictionary} with mappings\n
    \ttrailing_query >> the rest of the damn query
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, HASHMAP_FAILURE or HASHMAP_SUCCESS.\n
    <content> (if <result> is HASHMAP_SUCCESS) {Dictionary} containing table information.\n
    \t{"id": {...more key-values...}}
    """

    # second field: joins values of column_sql_translations if the value's key is found in column_names
    query = f"""
    SELECT {column_sql_translations['id']}, {', '.join(value for key, value in column_sql_translations.items() if key in column_names)}
    {trailing_query}
    """

    print(query)

    select = db_methods.safe_select(query=query, task=None, get_type='all')

    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.HASHMAP_FAILURE}

    # first array index is id
    # for rest of array, join column name(key) and rows(value)
    hash_map = {row[0]: dict(zip(column_names, row[1:]))
                for row in select['content']}
    
    return {'result': db_service_code_master.HASHMAP_SUCCESS, 'content': hash_map}
