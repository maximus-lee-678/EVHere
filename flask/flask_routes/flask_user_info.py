from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_user_info as db_user_info

# Other db_access imports
#


flask_user_info = Blueprint('flask_user_info', __name__, template_folder='flask_routes')


@flask_user_info.route('/api/login', methods=['POST'])
def fun_login():
    """
    | Endpoint implementation for <Route: Authenticate user login>

    :request POST fields: email, password

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_user_info.login_user`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # verify headers
    check_headers_response = flask_helper_functions.determine_json_existence(request.json, 'email', 'password')
    if check_headers_response['result'] != db_service_code_master.OPERATION_OK:
        return flask_helper_functions.format_for_endpoint(db_dictionary=check_headers_response,
                                                          success_scenarios_array=[])

    # authenticate user actual
    user_info_response = db_user_info.login_user(email_input=request.json['email'],
                                                 password_input=request.json['password'])

    return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                      success_scenarios_array=[db_service_code_master.LOGIN_SUCCESS])


@flask_user_info.route('/api/create_account', methods=['POST'])
def fun_create_account():
    """
    | Endpoint implementation for <Route: Create new user account>

    :request POST fields: username, password, email, full_name, phone_number

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_user_info.create_user`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # verify headers
    check_headers_response = flask_helper_functions.determine_json_existence(request.json, 'username', 'password', 'email', 'full_name', 'phone_number')
    if check_headers_response['result'] != db_service_code_master.OPERATION_OK:
        return flask_helper_functions.format_for_endpoint(db_dictionary=check_headers_response,
                                                          success_scenarios_array=[])

    # create user actual
    user_info_response = db_user_info.create_user(username_input=request.json['username'],
                                                  password_input=request.json['password'],
                                                  email_input=request.json['email'],
                                                  full_name_input=request.json['full_name'],
                                                  phone_no_input=request.json['phone_number'])

    return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                      success_scenarios_array=[db_service_code_master.USER_INFO_CREATE_SUCCESS])


@flask_user_info.route('/api/get_user_info', methods=['POST'])
def fun_get_user_info():
    """
    | Endpoint implementation for <Route: Get user account details>

    :request POST fields: email

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_user_info.get_user_id_by_email`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # verify headers
    check_headers_response = flask_helper_functions.determine_json_existence(request.json, 'email')
    if check_headers_response['result'] != db_service_code_master.OPERATION_OK:
        return flask_helper_functions.format_for_endpoint(db_dictionary=check_headers_response,
                                                          success_scenarios_array=[])

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=request.json['email'])
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # get user actual
    user_info_response = db_user_info.get_user_info_by_user_id(id_user_info_sanitised=id_user_info)

    return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                      success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])


@flask_user_info.route('/api/update_user_info', methods=['POST'])
def fun_update_user_info():
    """
    | Endpoint implementation for <Route: Update user account details>

    :request POST fields: email, email_new, full_name, username, phone_number, password

    :returns: Dictionary 

    | **Refer to:**
    | :meth:`db_access.db_user_info.update_user`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    # verify headers
    check_headers_response = flask_helper_functions.determine_json_existence(request.json, 'email', 'email_new', 'full_name', 'username', 'phone_number', 'password')
    if check_headers_response['result'] != db_service_code_master.OPERATION_OK:
        return flask_helper_functions.format_for_endpoint(db_dictionary=check_headers_response,
                                                          success_scenarios_array=[])

    # these fields may be zero-length strings, convert them to None if so
    phone_number = request.json['phone_number'] if request.json['phone_number'] != '' else None
    password = request.json['password'] if request.json['password'] != '' else None

    # get user id
    user_info_response = db_user_info.get_user_id_by_email(email_input=request.json['email'])
    if user_info_response['result'] != db_service_code_master.ACCOUNT_FOUND:
        return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                          success_scenarios_array=[db_service_code_master.ACCOUNT_FOUND])
    # store user id
    id_user_info = user_info_response['content']

    # update user actual
    user_info_response = db_user_info.update_user(id_user_info_sanitised=id_user_info, 
                                                  password_input=password,
                                                  email_input=request.json['email_new'], 
                                                  full_name_input=request.json['full_name'], 
                                                  username_input=request.json['username'], 
                                                  phone_no_input=phone_number)

    return flask_helper_functions.format_for_endpoint(db_dictionary=user_info_response,
                                                      success_scenarios_array=[db_service_code_master.USER_INFO_UPDATE_SUCCESS])
