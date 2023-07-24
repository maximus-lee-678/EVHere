from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_charger as db_charger

# Other db_access imports
import db_access.db_user_info as db_user_info


flask_charger = Blueprint('flask_charger', __name__,
                          template_folder='flask_routes')


@flask_charger.route('/api/get_all_chargers', methods=['POST'])
def fun_get_all_chargers():
    """
    | Endpoint implementation for <Route: Get all chargers>

    :request POST fields: email

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_charger.get_all_chargers_with_favourite_dict`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    email = request.json['email']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(
        email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # retrieve charger actual
    charger_response = db_charger.get_all_chargers_with_favourite_dict(
        id_user_info_sanitised=id_user_info)

    return flask_helper_functions.format_for_endpoint(db_dictionary=charger_response,
                                                      success_scenarios_array=[db_service_code_master.CHARGER_FOUND,
                                                                               db_service_code_master.CHARGER_NOT_FOUND])
