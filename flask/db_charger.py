import db_methods

def get_chargers():
    return db_methods.get_all_rows(table_name="charger", columns="name, latitude, longitude", where_column_name=None, sanitised_value=None)
