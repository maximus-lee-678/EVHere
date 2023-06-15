# Universal imports
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods

# Other db_access imports
#


def get_all_chargers(input_email):
    """
    Retrieves ALL chargers from database. If email is specified, adds an additional column indicating if charger is favourited.\n
    Returns Dictionary with keys:\n
    <result> CHARGER_NOT_FOUND or CHARGER_FOUND.\n
    <type> (if <result> is CHARGER_FOUND) CHARGER_WITH_FAVOURITE or CHARGER_WITHOUT_FAVOURITE.\n
    <content> (if <result> is CHARGER_FOUND) [{Dictionary Array}] containing charger information.\n
    \t"keys":\n
    \t{"id", "name", "latitude", "longitude", "address", "provider", "connectors", 
    "connector_types", "online", "kilowatts", "twenty_four_hours", "last_updated", "is_favourite"}
    """

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    # yes email
    if input_email is not None:
        # sanitise input
        email = db_helper_functions.string_sanitise(input_email)
        task = (email,)
        cursor.execute("""
        SELECT c.id, c.name, c.latitude, c.longitude, c.address, c.provider, c.connectors,
        GROUP_CONCAT(ct.name_short) AS connector_types, c.online, c.kilowatts, c.twenty_four_hours, 
        c.last_updated, CASE WHEN fc.id_user_info IS NULL THEN 0 ELSE 1 END AS is_favorite
        FROM charger AS c
        LEFT JOIN charger_available_connector AS cac ON c.id=cac.id_charger
        LEFT JOIN connector_type AS ct ON ct.id=cac.id_connector_type
        LEFT JOIN favourited_chargers AS fc ON c.id=fc.id_charger
        AND fc.id_user_info=(SELECT id FROM user_info WHERE email=?)
        GROUP BY c.id
        """, task)
    # no email
    else:
        cursor.execute("""
        SELECT c.id, c.name, c.latitude, c.longitude, c.address, c.provider, c.connectors,
        GROUP_CONCAT(ct.name_short) AS connector_types, c.online, c.kilowatts, c.twenty_four_hours, c.last_updated
        FROM charger AS c
        LEFT JOIN charger_available_connector AS cac ON c.id=cac.id_charger
        LEFT JOIN connector_type AS ct ON ct.id=cac.id_connector_type
        GROUP BY c.id
        """)

    rows = cursor.fetchall()
    db_methods.close_connection(conn)

    if db_methods.check_fetchall_has_nothing(rows):
        return {'result': db_service_code_master.CHARGER_NOT_FOUND}

    key_values = []
    # transforming array to key-values
    if input_email is not None:
        for row in rows:
            key_values.append({"id": row[0], "name": row[1], "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                               "connectors": row[6], "connector_types": str(row[7]).split(sep=","), "online": row[8], "kilowatts": row[9],
                               "twenty_four_hours": row[10], "last_updated": row[11], "is_favourite": row[12]})
    else:
        for row in rows:
            key_values.append({"id": row[0], "name": row[1], "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                               "connectors": row[6], "connector_types": str(row[7]).split(sep=","), "online": row[8], "kilowatts": row[9],
                               "twenty_four_hours": row[10], "last_updated": row[11]})

    return {'result': db_service_code_master.CHARGER_FOUND,
            'type': db_service_code_master.CHARGER_WITH_FAVOURITE
            if input_email != None else
            db_service_code_master.CHARGER_WITHOUT_FAVOURITE,
            'content': key_values}


def get_favourite_chargers(input_email):
    """
    Retrieves chargers that have been favourited by an email from the database.\n
    Returns Dictionary with keys:\n
    <result> CHARGER_NOT_FOUND or CHARGER_FOUND.\n
    <content> (if <result> is CHARGER_FOUND) [{Dictionary Array}] containing favourite charger information.\n
    \t"keys":\n
    \t{"id", "name", "latitude", "longitude", "address", "provider", "connectors", 
    "connector_types", "online", "kilowatts", "twenty_four_hours", "last_updated", "is_favourite"}
    """

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    # sanitise input
    email = db_helper_functions.string_sanitise(input_email)

    task = (email,)
    cursor.execute("""
    SELECT c.* FROM charger AS c
    LEFT JOIN favourited_chargers AS fc ON c.id=fc.id_charger
    WHERE fc.id_user_info=(SELECT id FROM user_info WHERE email=?)
    """, task)

    rows = cursor.fetchall()
    db_methods.close_connection(conn)

    if db_methods.check_fetchall_has_nothing(rows):
        return {'result': db_service_code_master.CHARGER_NOT_FOUND}

    key_values = []
    # transforming array to key-values
    for row in rows:
        key_values.append({"id": row[0], "name": row[1],
                           "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                           "connectors": row[6], "online": row[7], "kilowatts": row[8],
                           "twenty_four_hours": row[9], "last_updated": row[10]})

    return {'result': db_service_code_master.CHARGER_FOUND, 'content': key_values}


def get_one_charger(input_charger_id):
    """
    Retrieves a charger based on id from the database.\n
    Returns Dictionary with keys:\n
    <result> CHARGER_NOT_FOUND or CHARGER_FOUND.\n
    <content> (if <result> is CHARGER_FOUND) {Dictionary} containing single charger information.\n
    \t"keys":\n
    \t{"id", "name", "latitude", "longitude", "address", "provider", "connectors", 
    "connector_types", "online", "kilowatts", "twenty_four_hours", "last_updated", "is_favourite"}
    """

    # sanitise input
    charger_id = db_helper_functions.string_sanitise(input_charger_id)

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    task = (charger_id,)
    cursor.execute('SELECT * FROM charger WHERE id=?', task)

    row = cursor.fetchone()
    db_methods.close_connection(conn)

    if db_methods.check_fetchone_has_nothing(row):
        return {'result': db_service_code_master.CHARGER_NOT_FOUND}

    key_values = {"id": row[0], "name": row[1],
                  "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                  "connectors": row[6], "online": row[7], "kilowatts": row[8],
                  "twenty_four_hours": row[9], "last_updated": row[10]}

    return {'result': db_service_code_master.CHARGER_FOUND, 'content': key_values}
