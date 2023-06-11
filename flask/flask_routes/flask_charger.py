from flask import Blueprint, request

import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.db_charger as db_charger

flask_charger = Blueprint('flask_charger', __name__, template_folder='flask_routes')

# Route: Get all chargers
@flask_charger.route('/api/get_all_chargers', methods=['GET', 'POST'])
def fun_get_all_chargers():
    # if POST, should have email specified
    if request.method == 'POST':
        email = request.json['email']
        output = db_charger.get_all_chargers(input_email=email)
    # no email specified
    else:
        output = db_charger.get_all_chargers(input_email=None)

    if output['result'] == db_charger.CHARGER_NOT_FOUND:
        return {'success': False, 'api_response': db_charger.service_code_dict[output['result']]}

    return {'success': True, 'api_response': db_charger.service_code_dict[output['result']],
            'type': db_charger.service_code_dict[output['type']], 'content': output['content']}
