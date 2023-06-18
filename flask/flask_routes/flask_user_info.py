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

    # [FAILURE]
    if user_info_response['result'] != db_service_code_master.LOGIN_SUCCESS:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[user_info_response['result']],
                'reason': flask_helper_functions.join_strings(user_info_response['reason'], db_service_code_master.service_code_dict)}
    # [SUCCESS]
    return {'success': True,
            'api_response': db_service_code_master.service_code_dict[user_info_response['result']]}


# Route: Create new user account
@flask_user_info.route('/api/create_account', methods=['POST'])
def fun_create_account():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    full_name = request.json['full_name']
    phone_number = request.json['phone_number']

    # create user actual
    output = db_user_info.create_user(username_input=username, password_input=password,
                                      email_input=email, full_name_input=full_name, phone_no_input=phone_number)

    # [FAILURE]
    if output['result'] != db_service_code_master.USER_INFO_CREATE_SUCCESS:
        return {'success': False,
                'api_response': db_service_code_master.service_code_dict[output['result']],
                'reason': flask_helper_functions.join_strings(output['reason'], db_service_code_master.service_code_dict)}

    # [SUCCESS]
    return {'success': True,
            'api_response': db_service_code_master.service_code_dict[output['result']]}
