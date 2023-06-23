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
