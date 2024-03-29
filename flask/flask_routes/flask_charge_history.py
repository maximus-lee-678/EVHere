from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_charge_history as db_charge_history

# Other db_access imports
import db_access.db_user_info as db_user_info
import db_access.db_charge_current as db_charge_current


flask_charge_history = Blueprint('flask_charge_history', __name__, template_folder='flask_routes')


@flask_charge_history.route('/api/start_charge_history', methods=['POST'])
def fun_start_charge_history():
    """
    | Endpoint implementation for <Route: Start charging entry>

    :request POST fields: email, id_vehicle_info, id_charger, id_charger_available_connector

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_charge_history.add_charge_history_initial`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # verify headers
    check_headers_response = flask_helper_functions.determine_json_existence(request.json, 'email', 'id_vehicle_info', 'id_charger', 'id_charger_available_connector')
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

    # start charging history actual
    charge_history_response = db_charge_history.add_charge_history_initial(id_user_info_sanitised=id_user_info,
                                                                           id_vehicle_info_input=request.json['id_vehicle_info'],
                                                                           id_charger_input=request.json['id_charger'],
                                                                           id_charger_available_connector_input=request.json['id_charger_available_connector'])

    return flask_helper_functions.format_for_endpoint(db_dictionary=charge_history_response,
                                                      success_scenarios_array=[db_service_code_master.CHARGE_HISTORY_CREATE_SUCCESS])


@flask_charge_history.route('/api/finish_charge_history', methods=['POST'])
def fun_finish_charge_history():
    """
    | Endpoint implementation for <Route: Finish charging entry>

    :request POST fields: email, energy_drawn

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_charge_history.finish_charge_history`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # verify headers
    check_headers_response = flask_helper_functions.determine_json_existence(request.json, 'email', 'energy_drawn')
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

    # TODO replace with periodic automated updates
    # for now: override of current_energy_drawn
    charge_current_response = db_charge_current.update_user_charge_current(id_user_info_sanitised=id_user_info,
                                                                           current_energy_drawn_input=request.json['energy_drawn'])
    if charge_current_response['result'] != db_service_code_master.CHARGE_CURRENT_UPDATE_SUCCESS:
        return flask_helper_functions.format_for_endpoint(db_dictionary=charge_current_response,
                                                          success_scenarios_array=[db_service_code_master.CHARGE_CURRENT_UPDATE_SUCCESS])

    # finish charging history actual
    charge_history_response = db_charge_history.finish_charge_history(
        id_user_info_sanitised=id_user_info)

    return flask_helper_functions.format_for_endpoint(db_dictionary=charge_history_response,
                                                      success_scenarios_array=[db_service_code_master.CHARGE_HISTORY_FINISH_SUCCESS])


@flask_charge_history.route('/api/get_charge_history', methods=['POST'])
def fun_get_charge_history():
    """
    | Endpoint implementation for <Route: Get charge history (all)>

    :request POST fields: email, filter

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_charge_history.get_charge_history_by_user_id`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # verify headers
    check_headers_response = flask_helper_functions.determine_json_existence(request.json, 'email', 'filter')
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

    # get charging history actual
    charge_history_response = db_charge_history.get_charge_history_by_user_id(id_user_info_sanitised=id_user_info,
                                                                              filter_by=request.json['filter'])

    return flask_helper_functions.format_for_endpoint(db_dictionary=charge_history_response,
                                                      success_scenarios_array=[db_service_code_master.CHARGE_HISTORY_FOUND,
                                                                               db_service_code_master.CHARGE_HISTORY_NOT_FOUND])


# Route: Get charge history (currently charging)
@flask_charge_history.route('/api/get_charge_history_active', methods=['POST'])
def fun_get_charge_current():
    """
    | Endpoint implementation for <Route: Get charge history (currently charging)>

    :request POST fields: email

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_charge_history.get_charge_history_active`
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

    # get charge current actual
    charge_current_response = db_charge_history.get_charge_history_active(id_user_info_sanitised=id_user_info)

    return flask_helper_functions.format_for_endpoint(db_dictionary=charge_current_response,
                                                      success_scenarios_array=[db_service_code_master.CHARGE_HISTORY_FOUND,
                                                                               db_service_code_master.CHARGE_HISTORY_NOT_FOUND])
