from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_charge_history as db_charge_history

# Other db_access imports
import db_access.db_user_info as db_user_info
import db_access.db_charge_current as db_charge_current


flask_charge_history = Blueprint(
    'flask_charge_history', __name__, template_folder='flask_routes')


# Route: Start charging entry
@flask_charge_history.route('/api/start_charge_history', methods=['POST'])
def fun_start_charge_history():
    email = request.json['email']
    id_vehicle_info = request.json['id_vehicle_info']
    id_charger = request.json['id_charger']
    id_charger_available_connector = request.json['id_charger_available_connector']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # start charging history actual
    charge_history_response = db_charge_history.add_charge_history_initial(id_user_info_sanitised=id_user_info, id_vehicle_info_input=id_vehicle_info,
                                                                           id_charger_input=id_charger, id_charger_available_connector_input=id_charger_available_connector)

    return flask_helper_functions.format_for_endpoint(db_dictionary=charge_history_response,
                                                      success_scenarios_array=[db_service_code_master.CHARGE_HISTORY_CREATE_SUCCESS])


# Route: Finish charging entry
@flask_charge_history.route('/api/finish_charge_history', methods=['POST'])
def fun_finish_charge_history():
    email = request.json['email']
    energy_drawn = request.json['energy_drawn']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # TODO replace with periodic automated updates
    # for now: override of current_energy_drawn
    charge_current_response = db_charge_current.update_user_charge_current(id_user_info_sanitised=id_user_info, current_energy_drawn_input=energy_drawn)
    if charge_current_response['result'] != db_service_code_master.CHARGE_CURRENT_UPDATE_SUCCESS:
        return flask_helper_functions.format_for_endpoint(db_dictionary=charge_current_response,
                                                      success_scenarios_array=[db_service_code_master.CHARGE_CURRENT_UPDATE_SUCCESS])

    # finish charging history actual
    charge_history_response = db_charge_history.finish_charge_history(id_user_info_sanitised=id_user_info)
    
    return flask_helper_functions.format_for_endpoint(db_dictionary=charge_history_response,
                                                      success_scenarios_array=[db_service_code_master.CHARGE_HISTORY_FINISH_SUCCESS])


# Route: Get charge history (all)
@flask_charge_history.route('/api/get_charge_history', methods=['POST'])
def fun_get_charge_history():
    email = request.json['email']
    filter = request.json['filter']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # get charging history actual
    charge_history_response = db_charge_history.get_charge_history_by_user_id(id_user_info_sanitised=id_user_info, filter_by=filter)

    return flask_helper_functions.format_for_endpoint(db_dictionary=charge_history_response,
                                                      success_scenarios_array=[db_service_code_master.CHARGE_HISTORY_FOUND,
                                                                               db_service_code_master.CHARGE_HISTORY_NOT_FOUND])



# Route: Get charge history (currently charging)
@flask_charge_history.route('/api/get_charge_history_active', methods=['POST'])
def fun_get_charge_current():
    email = request.json['email']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # get charge current actual
    charge_current_response = db_charge_history.get_charge_history_active(
        id_user_info_sanitised=id_user_info)

    return flask_helper_functions.format_for_endpoint(db_dictionary=charge_current_response,
                                                      success_scenarios_array=[db_service_code_master.CHARGE_HISTORY_FOUND,
                                                                               db_service_code_master.CHARGE_HISTORY_NOT_FOUND])