from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_user_info as db_user_info

# Other db_access imports
#


flask_user_info = Blueprint(
    'flask_user_info', __name__, template_folder='flask_routes')


# Route: Authenticate user login
@flask_user_info.route('/api/login', methods=['POST'])
def fun_login():
    email = request.json['email']
    password = request.json['password']

    # authenticate user actual
    user_info_response = db_user_info.login_user(
        email_input=email, password_input=password)

    return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                      success_scenarios_array=[db_service_code_master.LOGIN_SUCCESS])


# Route: Create new user account
@flask_user_info.route('/api/create_account', methods=['POST'])
def fun_create_account():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    full_name = request.json['full_name']
    phone_number = request.json['phone_number']

    # create user actual
    user_info_response = db_user_info.create_user(username_input=username, password_input=password,
                                                  email_input=email, full_name_input=full_name, phone_no_input=phone_number)

    return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                      success_scenarios_array=[db_service_code_master.USER_INFO_CREATE_SUCCESS])


# Route: Get user account details
@flask_user_info.route('/api/get_user_info', methods=['POST'])
def fun_get_user_info():
    email = request.json['email']

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # get user actual
    user_info_response = db_user_info.get_user_info_by_user_id(
        id_user_info_sanitised=id_user_info)

    return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                      success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])


# Route: Update user account details
@flask_user_info.route('/api/update_user_info', methods=['POST'])
def fun_update_user_info():
    email = request.json['email']
    email_new = request.json['email_new']
    full_name = request.json['full_name']
    username = request.json['username']
    phone_number = request.json['phone_number'] if request.json['phone_number'] != '' else None
    password = request.json['password'] if request.json['password'] != '' else None

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=email)
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # update user actual
    user_info_response = db_user_info.update_user(id_user_info_sanitised=id_user_info, password_input=password,
                                                  email_input=email_new, full_name_input=full_name, username_input=username, phone_no_input=phone_number)

    return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                      success_scenarios_array=[db_service_code_master.USER_INFO_UPDATE_SUCCESS])
