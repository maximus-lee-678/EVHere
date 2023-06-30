from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_charge_current as db_charge_current

# Other db_access imports
import db_access.db_user_info as db_user_info


flask_charge_current = Blueprint(
    'db_charge_current', __name__, template_folder='flask_routes')


# Route: Get charge current
@flask_charge_current.route('/api/get_charge_current', methods=['POST'])
def fun_get_charge_current():
    email = request.json['email']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # get charge current actual
    charge_current_response = db_charge_current.get_charge_current_by_user_id_verbose(
        id_user_info_sanitised=id_user_info)

    return flask_helper_functions.format_for_endpoint(db_dictionary=charge_current_response,
                                                      success_scenarios_array=[db_service_code_master.CHARGE_CURRENT_FOUND,
                                                                               db_service_code_master.CHARGE_CURRENT_NOT_FOUND])
