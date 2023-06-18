from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_favourite_charger as db_favourite_charger

# Other db_access imports
import db_access.db_user_info as db_user_info
import db_access.db_charger as db_charger


flask_favourite_charger = Blueprint(
    'flask_favourite_charger', __name__, template_folder='flask_routes')


# Route: Get favourite chargers
@flask_favourite_charger.route('/api/get_favourite_chargers', methods=['POST'])
def fun_get_favourite_chargers():
    email = request.json['email']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[user_info_response['result']]}
    # store user id
    id_user_info = user_info_response['content']

    # retrieve favourite chargers actual
    favourite_charger_response = db_charger.get_favourite_chargers(user_id_sanitised=id_user_info)
    if favourite_charger_response['result'] != db_service_code_master.CHARGER_FOUND:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[favourite_charger_response['result']]}
    # deliver success payload
    return {'success': True,
            'api_response': db_service_code_master.service_code_dict[favourite_charger_response['result']],
            'content': favourite_charger_response['content']}


# Route: Add favourite charger
@flask_favourite_charger.route('/api/add_favourite_charger', methods=['POST'])
def fun_add_favourite_charger():
    email = request.json['email']
    id_charger = request.json['id_charger']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[user_info_response['result']]}
    # store user id
    id_user_info = user_info_response['content']

    # add favourite charger actual
    favourite_charger_response = db_favourite_charger.add_favourite_charger(
        id_user_info_sanitised=id_user_info, id_charger_input=id_charger)

    # [FAILURE]
    if favourite_charger_response['result'] != db_service_code_master.FAVOURITE_CHARGER_MODIFY_SUCCESS:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[favourite_charger_response['result']],
                'reason': flask_helper_functions.join_strings(favourite_charger_response['reason'], db_service_code_master.service_code_dict)}

    # [SUCCESS]
    return {'success': True,
            'api_response': db_service_code_master.service_code_dict[favourite_charger_response['result']]}


# Route: Remove favourite charger
@flask_favourite_charger.route('/api/remove_favourite_charger', methods=['POST'])
def fun_remove_favourite_charger():
    email = request.json['email']
    id_charger = request.json['id_charger']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[user_info_response['result']]}
    # store user id
    id_user_info = user_info_response['content']

    # add favourite charger actual
    favourite_charger_response = db_favourite_charger.remove_favourite_charger(
        id_user_info_sanitised=id_user_info, id_charger_input=id_charger)

    # [FAILURE]
    if favourite_charger_response['result'] != db_service_code_master.FAVOURITE_CHARGER_MODIFY_SUCCESS:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[favourite_charger_response['result']],
                'reason': flask_helper_functions.join_strings(favourite_charger_response['reason'], db_service_code_master.service_code_dict)}

    # [SUCCESS]
    return {'success': True,
            'api_response': db_service_code_master.service_code_dict[favourite_charger_response['result']]}
