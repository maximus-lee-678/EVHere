from flask import Blueprint, request

import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

import db_access.db_charger as db_charger
import db_access.db_favourite_charger as db_favourite_charger

flask_favourite_charger = Blueprint('flask_favourite_charger', __name__, template_folder='flask_routes')

# Route: Get favourite chargers
@flask_favourite_charger.route('/api/get_favourite_chargers', methods=['POST'])
def fun_get_favourite_chargers():
    email = request.json['email']

    output = db_charger.get_favourite_chargers(input_email=email)

    if output['result'] != db_service_code_master.CHARGER_FOUND:
        return {'success': False, 
                'api_response': db_service_code_master.service_code_dict[output['result']]}

    return {'success': True, 
            'api_response': db_service_code_master.service_code_dict[output['result']], 
            'content': output['content']}


# Route: Modify favourite charger (add/remove)
@flask_favourite_charger.route('/api/modify_favourite_charger', methods=['POST'])
def fun_modify_favourite_chargers():
    email = request.json['email']
    charger_id = request.json['charger_id']
    action = request.json['action']

    output = db_favourite_charger.modify_favourite_charger(
        input_email=email, input_charger_id=charger_id, input_action=action)

    if output['result'] != db_service_code_master.FAVOURITE_CHARGER_MODIFY_SUCCESS:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[output['result']],
                'reason': flask_helper_functions.join_strings(output['reason'], db_service_code_master.service_code_dict)}


    return {'success': True, 
            'api_response': db_service_code_master.service_code_dict[output['result']]}