# Universal imports
import db_access.support_files.db_helper_functions as db_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master
import db_access.support_files.db_methods as db_methods

# Other db_access imports
import db_access.db_user_info as db_user_info


def add_charge_history_initial(input_email, input_id_vehicle_info, input_id_charger, input_battery_percentage):
    """
    Attempts to insert a charge history into the database. This method will also add an entry to "charge current",
    as this method is called when the user starts a charge.\n
    Returns Dictionary with keys:\n
    <result> CHARGE_HISTORY_CREATE_FAILURE or CHARGE_HISTORY_CREATE_SUCCESS.\n
    <reason> (if <result> is CHARGE_HISTORY_CREATE_FAILURE) [Array] Reason for failure.
    \t[reasons]:\n
    \t[]
    """

    contains_errors = False
    error_list = []

    # 1.1: check if email exists
    user_response = db_user_info.get_user_id_by_email(input_email=input_email)
    if user_response['result'] == db_service_code_master.ACCOUNT_NOT_FOUND:
        contains_errors = True
        error_list.append(user_response['result'])
    # 1.2: store user id
    else:
        user_id = user_response['content']

    