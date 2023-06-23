from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_charge_history as db_charge_history

# Other db_access imports
import db_access.db_user_info as db_user_info


flask_charge_history = Blueprint(
    'flask_charge_history', __name__, template_folder='flask_routes')


# Route: Start charging entry
@flask_charge_history.route('/api/start_charge_history', methods=['POST'])
def fun_start_charge_history():
    email = request.json['email']
    id_vehicle_info = request.json['id_vehicle_info']
    id_charger = request.json['id_charger']
    battery_percentage = request.json['battery_percentage']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[user_info_response['result']]}
    # store user id
    id_user_info = user_info_response['content']

    # start charging history actual
    charge_history_response = db_charge_history.add_charge_history_initial(id_user_info_sanitised=id_user_info, id_vehicle_info_input=id_vehicle_info,
                                                                           id_charger_input=id_charger, battery_percentage_input=battery_percentage)

    # [FAILURE]
    if charge_history_response['result'] != db_service_code_master.CHARGE_HISTORY_CREATE_SUCCESS:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[charge_history_response['result']],
                'reason': flask_helper_functions.join_strings(charge_history_response['reason'], db_service_code_master.service_code_dict)}

    # [SUCCESS]
    return {'success': True,
            'api_response': db_service_code_master.service_code_dict[charge_history_response['result']]}


# Route: Finish charging entry
@flask_charge_history.route('/api/finish_charge_history', methods=['POST'])
def fun_finish_charge_history():
    email = request.json['email']
    battery_percentage = request.json['battery_percentage']
    amount_payable = request.json['amount_payable']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[user_info_response['result']]}
    # store user id
    id_user_info = user_info_response['content']

    # finish charging history actual
    charge_history_response = db_charge_history.finish_charge_history(id_user_info_sanitised=id_user_info,
                                                                      battery_percentage_input=battery_percentage, amount_payable_input=amount_payable)

    # [FAILURE]
    if charge_history_response['result'] != db_service_code_master.CHARGE_HISTORY_FINISH_SUCCESS:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[charge_history_response['result']],
                'reason': flask_helper_functions.join_strings(charge_history_response['reason'], db_service_code_master.service_code_dict)}

    # [SUCCESS]
    return {'success': True,
            'api_response': db_service_code_master.service_code_dict[charge_history_response['result']]}

# Route: Get charge history (in progress)
@flask_charge_history.route('/api/get_charge_history', methods=['POST'])
def fun_get_charge_history():
    email = request.json['email']
    filter = request.json['filter']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[user_info_response['result']]}
    # store user id
    id_user_info = user_info_response['content']

    # get charging history actual
    charge_history_response = db_charge_history.get_charge_history_by_user_id(id_user_info_sanitised=id_user_info, filter_by=filter)

     # [FAILURE]
    if charge_history_response['result'] != db_service_code_master.CHARGE_HISTORY_FOUND:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[charge_history_response['result']]}

    # [SUCCESS]
    return {'success': True,
            'api_response': db_service_code_master.service_code_dict[charge_history_response['result']],
            'content': charge_history_response['content']}