from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_vehicle as db_vehicle

# Other db_access imports
import db_access.db_user_info as db_user_info


flask_vehicle = Blueprint('flask_vehicle', __name__,
                          template_folder='flask_routes')


# Route: Get user's active vehicles
@flask_vehicle.route('/api/get_user_vehicles', methods=['POST'])
def fun_get_user_vehicles():
    email = request.json['email']

    # get user id
    user_id_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_id_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[user_id_response['result']]}
    # store user id
    id_user_info = user_id_response['content']

    # get user vehicles actual
    vehicle_response = db_vehicle.get_active_vehicle_by_user_id(
        id_user_info_sanitised=id_user_info)

    # [FAILURE]
    if vehicle_response['result'] != db_service_code_master.VEHICLE_FOUND:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[vehicle_response['result']]}

    # [SUCCESS]
    return {'success': True,
            'api_response': db_service_code_master.service_code_dict[vehicle_response['result']],
            'content': vehicle_response['content']}


# Route: Add new vehicle
@flask_vehicle.route('/api/add_vehicle', methods=['POST'])
def fun_add_vehicle():
    email = request.json['email']
    vehicle_name = request.json['vehicle_name']
    vehicle_model = request.json['vehicle_model']
    vehicle_sn = request.json['vehicle_sn']
    vehicle_connector = request.json['vehicle_connector']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[user_info_response['result']]}
    # store user id
    id_user_info = user_info_response['content']

    # add vehicle actual
    vehicle_response = db_vehicle.add_vehicle(
        id_user_info_sanitised=id_user_info, name_input=vehicle_name, model_input=vehicle_model,
        sn_input=vehicle_sn, connector_input=vehicle_connector)

    # [FAILURE]
    if vehicle_response['result'] != db_service_code_master.VEHICLE_ADD_SUCCESS:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[vehicle_response['result']],
                'reason': flask_helper_functions.join_strings(vehicle_response['reason'], db_service_code_master.service_code_dict)}

    # [SUCCESS]
    return {'success': True,
            'api_response': db_service_code_master.service_code_dict[vehicle_response['result']]}


# Route: Remove vehicle
@flask_vehicle.route('/api/remove_vehicle', methods=['POST'])
def fun_remove_vehicle():
    id_vehicle = request.json['id_vehicle']

    # remove vehicle actual
    vehicle_response = db_vehicle.remove_vehicle(id_vehicle_input=id_vehicle)

    # [FAILURE]
    if vehicle_response['result'] != db_service_code_master.VEHICLE_REMOVE_SUCCESS:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[vehicle_response['result']],
                'reason': flask_helper_functions.join_strings(vehicle_response['reason'], db_service_code_master.service_code_dict)}

    # [SUCCESS]
    return {'success': True,
            'api_response': db_service_code_master.service_code_dict[vehicle_response['result']]}
