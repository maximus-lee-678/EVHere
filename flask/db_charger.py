import db_methods
import helper_functions

MISSING_FIELDS = 1

ALL_WITH_FAVOURITE = 100
ALL_WITHOUT_FAVOURITE = 101
CHARGER_FOUND = 102
CHARGER_NOT_FOUND = 103

service_code_dict = {
    ALL_WITH_FAVOURITE: "Contains is_favourite.",
    ALL_WITHOUT_FAVOURITE: "No favourites.",
    CHARGER_FOUND: "Found chargers.",
    CHARGER_NOT_FOUND: "No matching chargers found."
}


def get_all_chargers(input_email):
    """
    Retrieves ALL chargers from database. If email is specified, adds an additional column indicating if charger is favourited.\n
    Returns Dictionary with keys:\n
    <result> CHARGER_NOT_FOUND or CHARGER_FOUND.\n
    <type> (if <result> is CHARGER_FOUND) ALL_WITH_FAVOURITE or ALL_WITHOUT_FAVOURITE.\n
    <content> (if <result> is CHARGER_FOUND) Dictionary containing charger information.
    """

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    # yes email
    if input_email is not None:
        # sanitise input
        email = helper_functions.string_sanitise(input_email)
        task = (email,)
        cursor.execute("""
        SELECT c.*, CASE WHEN fc.id_user_info IS NULL THEN 0 ELSE 1 END AS is_favorite
        FROM charger AS c
        LEFT JOIN favourited_chargers AS fc ON c.id=fc.id_charger
        AND fc.id_user_info=(SELECT id FROM user_info WHERE email=?)
        """, task)
    # no email
    else:
        cursor.execute('SELECT * FROM charger')

    rows = cursor.fetchall()
    db_methods.close_connection(conn)

    if db_methods.check_fetchall(rows):
        return {'result': CHARGER_NOT_FOUND}

    key_values = []
    # transforming array to key-values
    if input_email is not None:
        for row in rows:
            key_values.append({"id": row[0], "name": row[1],
                               "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                               "connectors": row[6], "online": row[7], "kilowatts": row[8],
                               "twenty_four_hours": row[9], "last_updated": row[10], "is_favourite": row[11]})
    else:
        for row in rows:
            key_values.append({"id": row[0], "name": row[1],
                               "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                               "connectors": row[6], "online": row[7], "kilowatts": row[8],
                               "twenty_four_hours": row[9], "last_updated": row[10]})

    return {'result': CHARGER_FOUND,
            'type': ALL_WITH_FAVOURITE if input_email != None else ALL_WITHOUT_FAVOURITE,
            'content': key_values}


def get_favourite_chargers(input_email):
    """
    Retrieves chargers that have been favourited by an email from the database.\n
    Returns Dictionary with keys:\n
    <result> MISSING_FIELDS, CHARGER_NOT_FOUND or CHARGER_FOUND.\n
    <content> (if <result> is CHARGER_FOUND) Dictionary containing favourite charger information.
    """

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    # sanitise input
    email = helper_functions.string_sanitise(input_email)

    task = (email,)
    cursor.execute("""
    SELECT c.* FROM charger AS c
    LEFT JOIN favourited_chargers AS fc ON c.id=fc.id_charger
    WHERE fc.id_user_info=(SELECT id FROM user_info WHERE email=?)
    """, task)

    rows = cursor.fetchall()
    db_methods.close_connection(conn)

    if db_methods.check_fetchall(rows):
        return {'result': CHARGER_NOT_FOUND}

    key_values = []
    # transforming array to key-values
    for row in rows:
        key_values.append({"id": row[0], "name": row[1],
                           "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                           "connectors": row[6], "online": row[7], "kilowatts": row[8],
                           "twenty_four_hours": row[9], "last_updated": row[10]})

    return {'result': CHARGER_FOUND, 'content': key_values}


def get_one_charger(input_charger_id):
    """
    Retrieves a charger based on id from the database.\n
    Returns Dictionary with keys:\n
    <result> CHARGER_NOT_FOUND or CHARGER_FOUND.\n
    <content> (if <result> is CHARGER_FOUND) Array containing single charger information.
    """

    # sanitise input
    charger_id = helper_functions.string_sanitise(input_charger_id)

    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    task = (charger_id,)
    cursor.execute('SELECT * FROM charger WHERE id=?', task)

    row = cursor.fetchone()
    db_methods.close_connection(conn)

    if db_methods.check_fetchone(row):
        return {'result': CHARGER_NOT_FOUND}

    return {'result': CHARGER_FOUND, 'content': row}
