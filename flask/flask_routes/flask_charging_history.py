from flask import Blueprint, request

import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.db_charge_history as db_charge_history

flask_charging_history = Blueprint(
    'flask_charging_history', __name__, template_folder='flask_routes')


# Route: Start charging entry
@flask_charging_history.route('/api/start_charge', methods=['POST'])
def start_charge():
    email = request.json['email']
    id_vehicle_info = request.json['id_vehicle_info']
    id_charger = request.json['id_charger']
    battery_percentage = request.json['battery_percentage']

    output = db_charge_history.add_charge_history_initial(input_email=email, input_id_vehicle_info=id_vehicle_info,
                                                          input_id_charger=id_charger, input_battery_percentage=battery_percentage)

    if output['result'] != db_charge_history.CONNECTOR_FOUND:
        return {'success': False, 'api_response': db_charge_history.service_code_dict[output['result']]}

    return {'success': True, 'api_response': db_charge_history.service_code_dict[output['result']], 'content': output['content']}
