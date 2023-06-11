from flask import Blueprint, request

import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.db_vehicle as db_vehicle

flask_vehicle = Blueprint('flask_vehicle', __name__, template_folder='flask_routes')

# Route: Get user's active vehicles
@flask_vehicle.route('/api/get_user_vehicles', methods=['POST'])
def fun_get_user_vehicles():
    email = request.json['email']

    output = db_vehicle.get_active_vehicle_by_email(input_email=email)

    if output['result'] == db_vehicle.VEHICLE_NOT_FOUND:
        return {'success': False, 'api_response': db_vehicle.service_code_dict[output['result']]}

    return {'success': True, 'api_response': db_vehicle.service_code_dict[output['result']], 'content': output['content']}


# Route: Add new vehicle
@flask_vehicle.route('/api/add_vehicle', methods=['POST'])
def fun_add_vehicle():
    email = request.json['email']
    vehicle_name = request.json['vehicle_name']
    vehicle_model = request.json['vehicle_model']
    vehicle_sn = request.json['vehicle_sn']
    vehicle_connector = request.json['vehicle_connector']

    output = db_vehicle.add_vehicle(
        input_email=email, input_vehicle_name=vehicle_name, input_vehicle_model=vehicle_model, input_vehicle_sn=vehicle_sn, input_vehicle_connector=vehicle_connector)

    if output['result'] == db_vehicle.ADD_FAILURE:
        return {'success': False, 'api_response': db_vehicle.service_code_dict[output['result']],
                'reason': flask_helper_functions.join_strings(output['reason'], db_vehicle.service_code_dict)}

    return {'success': True, 'api_response': db_vehicle.service_code_dict[output['result']]}

# Route: Remove vehicle
@flask_vehicle.route('/api/remove_vehicle', methods=['POST'])
def fun_remove_vehicle():
    vehicle_id = request.json['vehicle_id']

    output = db_vehicle.remove_vehicle(input_vehicle_id=vehicle_id)

    if output['result'] == db_vehicle.REMOVE_FAILURE:
        return {'success': False, 'api_response': db_vehicle.service_code_dict[output['result']],
                'reason': flask_helper_functions.join_strings(output['reason'], db_vehicle.service_code_dict)}

    return {'success': True, 'api_response': db_vehicle.service_code_dict[output['result']]}
