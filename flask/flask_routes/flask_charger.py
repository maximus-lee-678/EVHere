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


# Route: Get all chargers
@flask_charger.route('/api/get_all_chargers', methods=['GET', 'POST'])
def fun_get_all_chargers():
    # if POST, email will be specified
    if request.method == 'POST':
        email = request.json['email']

        # get user id
        user_info_response = db_user_info.get_user_id_by_email(email_input=email)
        if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
            return {'success': False,
                    'api_response': db_service_code_master.service_code_dict[user_info_response['result']]}
        # store user id
        id_user_info = user_info_response['content']

        # retrieve charger actual
        charger_response = db_charger.get_all_chargers(
            user_id_sanitised=id_user_info)
    
    # if GET, no email, and by extension user id, is specified
    else:
        # retrieve charger actual 2
        charger_response = db_charger.get_all_chargers(user_id_sanitised=None)

    # [FAILURE]
    if charger_response['result'] != db_service_code_master.CHARGER_FOUND:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[charger_response['result']]}

    # [SUCCESS]
    return {'success': True,
            'api_response': db_service_code_master.service_code_dict[charger_response['result']],
            'type': db_service_code_master.service_code_dict[charger_response['type']],
            'content': charger_response['content']}
