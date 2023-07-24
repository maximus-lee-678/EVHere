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
            return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                            success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
        # store user id
        id_user_info = user_info_response['content']

        # retrieve charger actual
        charger_response = db_charger.get_all_chargers(
            id_user_info_sanitised=id_user_info)
    
    # if GET, no email, and by extension user id, is specified
    else:
        # retrieve charger actual 2
        charger_response = db_charger.get_all_chargers(id_user_info_sanitised=None)

    return flask_helper_functions.format_for_endpoint(db_dictionary=charger_response,
                                                    success_scenarios_array=[db_service_code_master.CHARGER_FOUND,
                                                                             db_service_code_master.CHARGER_NOT_FOUND])

@flask_charger.route('/api/update_charger/', methods=['POST'])
def fun_update_charger():
    id = request.json['id']
    pv_current_in=request.json['pv_current_in'] 
    pv_energy_level=request.json['pv_energy_level']
    pv_timestamp = request.json['pv_timestamp']
    charger_response = db_charger.get_charger_by_id(id)
    # store charger
    charger_info = charger_response['content'][0]
    # update charger
    charger_info_response = db_charger.update_charger(charger = charger_info, pv_current_in=pv_current_in,
                                                  pv_energy_level=pv_energy_level, pv_timestamp=pv_timestamp)
    print(charger_info_response['content'])
    return flask_helper_functions.format_for_endpoint(db_dictionary=charger_info_response, success_scenarios_array=[db_service_code_master.CHARGER_FOUND,
                                                                             db_service_code_master.CHARGER_NOT_FOUND])