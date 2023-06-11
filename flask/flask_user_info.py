from __main__ import app, request

import helper_functions
import db_user_info

@app.route('/api/login', methods=['POST'])  # Route: Authenticate user login
def fun_login():
    email = request.json['email']
    password = request.json['password']

    output = db_user_info.login_user(
        input_email=email, input_password=password)

    if output['result'] == db_user_info.LOGIN_FAILURE:
        return {'success': False, 'api_response': db_user_info.service_code_dict[output['result']], 'reason': db_user_info.service_code_dict[output['reason']]}

    return {'success': True, 'api_response': db_user_info.service_code_dict[output['result']]}


# Route: Create new user account
@app.route('/api/create_account', methods=['POST'])
def fun_create_account():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    full_name = request.json['full_name']
    phone_number = request.json['phone_number']

    output = db_user_info.create_user(input_username=username, input_password=password,
                                      input_email=email, input_full_name=full_name, input_phone_no=phone_number)

    if output['result'] == db_user_info.CREATE_FAILURE:
        return {'success': False, 'api_response': db_user_info.service_code_dict[output['result']],
                'reason': helper_functions.join_strings(output['reason'], db_user_info.service_code_dict)}

    return {'success': True, 'api_response': db_user_info.service_code_dict[output['result']]}