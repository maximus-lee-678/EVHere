# Universal imports
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods

# Other db_access imports
import db_access.db_universal as db_universal


def get_all_chargers_hash_map(
    column_names=['name', 'latitude', 'longitude', 'address', 'provider',
                           'connectors', 'connector_types', 'online', 'kilowatts', 'twenty_four_hours', 'last_updated']
):
    """
    Full:
    SELECT c.id, c.name, c.latitude, c.longitude, c.address, c.provider, c.connectors,
    GROUP_CONCAT(ct.name_short) AS connector_types, c.online, c.kilowatts, c.twenty_four_hours, c.last_updated
    FROM charger AS c
    LEFT JOIN charger_available_connector AS cac ON c.id=cac.id_charger
    LEFT JOIN connector_type AS ct ON ct.id=cac.id_connector_type
    GROUP BY c.id
    """
    column_sql_translations = {'id': 'c.id', 'name': 'c.name', 'latitude': 'c.latitude', 'longitude': 'c.longitude',
                               'address': 'c.address', 'provider': 'c.provider', 'connectors': 'c.connectors',
                               'connector_types': 'GROUP_CONCAT(ct.name_short) AS connector_types', 'online': 'c.online',
                               'kilowatts': 'c.kilowatts', 'twenty_four_hours': 'c.twenty_four_hours', 'last_updated': 'c.last_updated'}

    trailing_query = """
    FROM charger AS c
    LEFT JOIN charger_available_connector AS cac ON c.id=cac.id_charger
    LEFT JOIN connector_type AS ct ON ct.id=cac.id_connector_type
    LEFT JOIN favourited_chargers AS fc ON c.id=fc.id_charger
    GROUP BY c.id
    """

    return db_universal.get_all_universal_hash_map(column_names=column_names,
                                                   column_sql_translations=column_sql_translations,
                                                   trailing_query=trailing_query)


def get_all_chargers(user_id_sanitised):
    """
    Retrieves ALL chargers from database. If user id is specified, adds an additional column indicating if charger is favourited.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CHARGER_NOT_FOUND or CHARGER_FOUND.\n
    <type> (if <result> is CHARGER_FOUND) CHARGER_WITH_FAVOURITE or CHARGER_WITHOUT_FAVOURITE.\n
    <content> (if <result> is CHARGER_FOUND) [{Dictionary Array}] containing charger information.\n
    \t"keys":\n
    \t{"id", "name", "latitude", "longitude", "address", "provider", "connectors", 
    "connector_types", "online", "kilowatts", "twenty_four_hours", "last_updated", "is_favourite"}
    """

    get_all_chargers_hash_map()

    if user_id_sanitised is not None:
        query = """
        SELECT c.id, c.name, c.latitude, c.longitude, c.address, c.provider, c.connectors,
        GROUP_CONCAT(ct.name_short) AS connector_types, c.online, c.kilowatts, c.twenty_four_hours, 
        c.last_updated, CASE WHEN fc.id_user_info IS NULL THEN 0 ELSE 1 END AS is_favorite
        FROM charger AS c
        LEFT JOIN charger_available_connector AS cac ON c.id=cac.id_charger
        LEFT JOIN connector_type AS ct ON ct.id=cac.id_connector_type
        LEFT JOIN favourited_chargers AS fc ON c.id=fc.id_charger
        AND fc.id_user_info=?
        GROUP BY c.id
        """
        task = (user_id_sanitised,)

        select = db_methods.safe_select(query=query, task=task, get_type='all')

    # no get user favourites
    else:
        query = """
        SELECT c.id, c.name, c.latitude, c.longitude, c.address, c.provider, c.connectors,
        GROUP_CONCAT(ct.name_short) AS connector_types, c.online, c.kilowatts, c.twenty_four_hours, c.last_updated
        FROM charger AS c
        LEFT JOIN charger_available_connector AS cac ON c.id=cac.id_charger
        LEFT JOIN connector_type AS ct ON ct.id=cac.id_connector_type
        GROUP BY c.id
        """

        select = db_methods.safe_select(query=query, task=None, get_type='all')

    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.CHARGER_NOT_FOUND}

    # transforming array to key-values
    if user_id_sanitised is not None:
        key_values = [{"id": row[0], "name": row[1], "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                       "connectors": row[6], "connector_types": str(row[7]).split(sep=","), "online": row[8], "kilowatts": row[9],
                       "twenty_four_hours": row[10], "last_updated": row[11], "is_favourite": row[12]}
                      for row in select['content']]
    else:
        key_values = [{"id": row[0], "name": row[1], "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                       "connectors": row[6], "connector_types": str(row[7]).split(sep=","), "online": row[8], "kilowatts": row[9],
                       "twenty_four_hours": row[10], "last_updated": row[11]}
                      for row in select['content']]

    return {'result': db_service_code_master.CHARGER_FOUND,
            'type': db_service_code_master.CHARGER_WITH_FAVOURITE
            if user_id_sanitised != None else
            db_service_code_master.CHARGER_WITHOUT_FAVOURITE,
            'content': key_values}


def get_favourite_chargers(user_id_sanitised):
    """
    Retrieves chargers that have been favourited by a user from the database.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CHARGER_NOT_FOUND or CHARGER_FOUND.\n
    <content> (if <result> is CHARGER_FOUND) [{Dictionary Array}] containing favourite charger information.\n
    \t"keys":\n
    \t{"id", "name", "latitude", "longitude", "address", "provider", "connectors", 
    "connector_types", "online", "kilowatts", "twenty_four_hours", "last_updated", "is_favourite"}
    """
    query = """
    SELECT c.* FROM charger AS c
    LEFT JOIN favourited_chargers AS fc ON c.id=fc.id_charger
    WHERE fc.id_user_info=?
    """
    task = (user_id_sanitised,)

    select = db_methods.safe_select(query=query, task=task, get_type='all')

    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.CHARGER_NOT_FOUND}

    # transforming array to key-values
    key_values = [{"id": row[0], "name": row[1],
                   "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                   "connectors": row[6], "online": row[7], "kilowatts": row[8],
                   "twenty_four_hours": row[9], "last_updated": row[10]}
                  for row in select['content']]

    return {'result': db_service_code_master.CHARGER_FOUND, 'content': key_values}


def get_one_charger(id_charger_input):
    """
    Retrieves a charger based on id from the database.\n
    Returns Dictionary with keys:\n
    <result> INTERNAL_ERROR, CHARGER_NOT_FOUND or CHARGER_FOUND.\n
    <content> (if <result> is CHARGER_FOUND) {Dictionary} containing single charger information.\n
    \t"keys":\n
    \t{"id", "name", "latitude", "longitude", "address", "provider", "connectors", 
    "connector_types", "online", "kilowatts", "twenty_four_hours", "last_updated", "is_favourite"}
    """

    # sanitise input
    id_charger_sanitised = db_helper_functions.string_sanitise(
        id_charger_input)

    query = 'SELECT * FROM charger WHERE id=?'
    task = (id_charger_sanitised,)

    select = db_methods.safe_select(query=query, task=task, get_type='one')

    if not select['select_successful']:
        return {'result': db_service_code_master.INTERNAL_ERROR}
    if select['num_rows'] == 0:
        return {'result': db_service_code_master.CHARGER_NOT_FOUND}

    # transforming row to key-values
    key_values = {"id": select['content'][0], "name": select['content'][1], "latitude": select['content'][2],
                  "longitude": select['content'][3], "address": select['content'][4], "provider": select['content'][5],
                  "connectors": select['content'][6], "online": select['content'][7], "kilowatts": select['content'][8],
                  "twenty_four_hours": select['content'][9], "last_updated": select['content'][10]}

    return {'result': db_service_code_master.CHARGER_FOUND, 'content': key_values}
