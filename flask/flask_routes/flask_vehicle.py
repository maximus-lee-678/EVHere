from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_vehicle as db_vehicle

# Other db_access imports
import db_access.db_user_info as db_user_info


flask_vehicle = Blueprint('flask_vehicle', __name__, template_folder='flask_routes')


@flask_vehicle.route('/api/get_user_vehicles', methods=['POST'])
def fun_get_user_vehicles():
    """
    | Endpoint implementation for <Route: Get user's active vehicles>

    :request POST fields: email

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_vehicle.get_active_vehicle_by_user_id`
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

    # get user vehicles actual
    vehicle_response = db_vehicle.get_active_vehicle_by_user_id(id_user_info_sanitised=id_user_info)

    return flask_helper_functions.format_for_endpoint(db_dictionary=vehicle_response,
                                                      success_scenarios_array=[db_service_code_master.VEHICLE_FOUND,
                                                                               db_service_code_master.VEHICLE_NOT_FOUND])


@flask_vehicle.route('/api/add_vehicle', methods=['POST'])
def fun_add_vehicle():
    """
    | Endpoint implementation for <Route: Add new vehicle>

    :request POST fields: email, vehicle_name, vehicle_model, vehicle_sn, vehicle_connector

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_vehicle.add_vehicle`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # verify headers
    check_headers_response = flask_helper_functions.determine_json_existence(request.json, 'email', 'vehicle_name', 'vehicle_model', 'vehicle_sn', 'vehicle_connector')
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

    # add vehicle actual
    vehicle_response = db_vehicle.add_vehicle(id_user_info_sanitised=id_user_info,
                                              name_input=request.json['vehicle_name'],
                                              model_input=request.json['vehicle_model'],
                                              sn_input=request.json['vehicle_sn'],
                                              connector_input=request.json['vehicle_connector'])

    return flask_helper_functions.format_for_endpoint(db_dictionary=vehicle_response,
                                                      success_scenarios_array=[db_service_code_master.VEHICLE_ADD_SUCCESS])


# Route: Remove vehicle
@flask_vehicle.route('/api/remove_vehicle', methods=['POST'])
def fun_remove_vehicle():
    """
    | Endpoint implementation for <Route: Remove vehicle>

    :request POST fields: id_vehicle

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_vehicle.remove_vehicle`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # verify headers
    check_headers_response = flask_helper_functions.determine_json_existence(request.json, 'email', 'id_vehicle')
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

    # remove vehicle actual
    vehicle_response = db_vehicle.remove_vehicle(id_user_info_sanitised=id_user_info, id_vehicle_input=request.json['id_vehicle'])

    return flask_helper_functions.format_for_endpoint(db_dictionary=vehicle_response,
                                                      success_scenarios_array=[db_service_code_master.VEHICLE_REMOVE_SUCCESS])
