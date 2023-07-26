from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_favourite_charger as db_favourite_charger

# Other db_access imports
import db_access.db_user_info as db_user_info


flask_favourite_charger = Blueprint('flask_favourite_charger', __name__, template_folder='flask_routes')


@flask_favourite_charger.route('/api/get_favourite_chargers', methods=['POST'])
def fun_get_favourite_chargers():
    """
    | Endpoint implementation for <Route: Get favourite chargers>

    :request POST fields: email

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_favourite_charger.get_user_favourite_chargers`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # verify headers
    check_headers_response = flask_helper_functions.determine_json_existence(request.json, 'email')
    if check_headers_response['result'] != db_service_code_master.OPERATION_OK:
        return flask_helper_functions.format_for_endpoint(db_dictionary=check_headers_response,
                                                          success_scenarios_array=[])

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=request.json['email'])
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # retrieve favourite chargers actual
    favourite_charger_response = db_favourite_charger.get_user_favourite_chargers(id_user_info_sanitised=id_user_info)

    return flask_helper_functions.format_for_endpoint(db_dictionary=favourite_charger_response,
                                                      success_scenarios_array=[db_service_code_master.FAVOURITE_CHARGERS_NOT_FOUND,
                                                                               db_service_code_master.FAVOURITE_CHARGERS_FOUND])


@flask_favourite_charger.route('/api/add_favourite_charger', methods=['POST'])
def fun_add_favourite_charger():
    """
    | Endpoint implementation for <Route: Add favourite charger>

    :request POST fields: email, id_charger

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_favourite_charger.add_favourite_charger`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # verify headers
    check_headers_response = flask_helper_functions.determine_json_existence(request.json, 'email', 'id_charger')
    if check_headers_response['result'] != db_service_code_master.OPERATION_OK:
        return flask_helper_functions.format_for_endpoint(db_dictionary=check_headers_response,
                                                          success_scenarios_array=[])

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=request.json['email'])
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # add favourite charger actual
    favourite_charger_response = db_favourite_charger.add_favourite_charger(id_user_info_sanitised=id_user_info,
                                                                            id_charger_input=request.json['id_charger'])

    return flask_helper_functions.format_for_endpoint(db_dictionary=favourite_charger_response,
                                                      success_scenarios_array=[db_service_code_master.FAVOURITE_CHARGER_MODIFY_SUCCESS])


@flask_favourite_charger.route('/api/remove_favourite_charger', methods=['POST'])
def fun_remove_favourite_charger():
    """
    | Endpoint implementation for <Route: Remove favourite charger>

    :request POST fields: email, id_charger

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_favourite_charger.remove_favourite_charger`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # verify headers
    check_headers_response = flask_helper_functions.determine_json_existence(request.json, 'email', 'id_charger')
    if check_headers_response['result'] != db_service_code_master.OPERATION_OK:
        return flask_helper_functions.format_for_endpoint(db_dictionary=check_headers_response,
                                                          success_scenarios_array=[])

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=request.json['email'])
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # add favourite charger actual
    favourite_charger_response = db_favourite_charger.remove_favourite_charger(id_user_info_sanitised=id_user_info,
                                                                               id_charger_input=request.json['id_charger'])

    return flask_helper_functions.format_for_endpoint(db_dictionary=favourite_charger_response,
                                                      success_scenarios_array=[db_service_code_master.FAVOURITE_CHARGER_MODIFY_SUCCESS])
