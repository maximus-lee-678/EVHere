import db_methods
import helper_functions

def get_all_chargers(input_email):
    conn = db_methods.setup_connection()
    cursor = conn.cursor()

    if input_email is not None:
        email = helper_functions.string_sanitise(input_email)
        task = (email,)
        cursor.execute("""SELECT c.id, c.name, c.latitude, c.longitude, CASE WHEN fc.id_user_info IS NULL THEN 0 ELSE 1 END AS is_favorite
                    FROM charger AS c
                    LEFT JOIN favourited_chargers AS fc ON c.id=fc.id_charger
                    AND fc.id_user_info=(SELECT id FROM user_info WHERE email=?)
                    """, task)
    else:
        cursor.execute("""SELECT c.id, c.name, c.latitude, c.longitude
                    FROM charger AS c""")
        
    rows = cursor.fetchall()
    db_methods.close_connection(conn)

    return rows
