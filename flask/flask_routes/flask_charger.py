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


@flask_charger.route('/api/get_all_chargers', methods=['GET', 'POST'])
def fun_get_all_chargers():
    """
    | Endpoint implementation for <Route: Get all chargers>

    :request POST fields: email

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_charger.get_all_chargers_with_favourite_dict`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # if POST, email will be specified
    if request.method == 'POST':
        email = request.json['email']

        # get user id
        user_info_response = db_user_info.get_user_id_by_email(
            email_input=email)
        if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
            return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                              success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
        # store user id
        id_user_info = user_info_response['content']

        # retrieve charger actual
        charger_response = db_charger.get_all_chargers_dict_join_favourite(
            id_user_info_sanitised=id_user_info)

    # if GET, no email, and by extension user id, is specified
    else:
        # retrieve charger actual 2
        charger_response = db_charger.get_all_chargers_dict_join_favourite(
            id_user_info_sanitised=None)

    return flask_helper_functions.format_for_endpoint(db_dictionary=charger_response,
                                                      success_scenarios_array=[db_service_code_master.CHARGER_FOUND,
                                                                               db_service_code_master.CHARGER_NOT_FOUND])


@flask_charger.route('/api/update_charger/', methods=['POST'])
def fun_update_charger():
    """
    | Endpoint implementation for <Route: Update charger>

    :request POST fields: id_charger, pv_voltage_in*, pv_current_in*, pv_voltage_out*, pv_current_out*, rate_predicted*

    (fields marked with * are not compulsory.)

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_charger.update_charger_technical`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    id_charger = request.json['id_charger']

    fields_to_update = {}

    if 'pv_voltage_in' in request.json:
        fields_to_update.update(
            {"pv_voltage_in": request.json['pv_voltage_in']})
    if 'pv_current_in' in request.json:
        fields_to_update.update(
            {"pv_current_in": request.json['pv_current_in']})
    if 'pv_voltage_out' in request.json:
        fields_to_update.update(
            {"pv_voltage_out": request.json['pv_voltage_out']})
    if 'pv_current_out' in request.json:
        fields_to_update.update(
            {"pv_current_out": request.json['pv_current_out']})
    if 'rate_predicted' in request.json:
        fields_to_update.update(
            {"rate_predicted": request.json['rate_predicted']})

    # update charger actual
    charger_info_response = db_charger.update_charger_technical(
        id_charger=id_charger, fields_to_update=fields_to_update)

    return flask_helper_functions.format_for_endpoint(db_dictionary=charger_info_response, success_scenarios_array=[db_service_code_master.CHARGER_UPDATE_SUCCESS])
