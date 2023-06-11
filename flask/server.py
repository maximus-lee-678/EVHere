# Import flask and datetime module for showing date and time
from flask import Flask, request
from flask_cors import CORS
import os

import helper_functions
import db_user_info
import db_methods
import db_charger
import db_favourite_charger
import db_connector_type
import db_vehicle

# If db file not exists, create
if not os.path.exists(db_methods.DATABASE_PATH):
    db_methods.touch_database()
    print(
        f"[!] database not found, created new database at {db_methods.DATABASE_PATH}!")

# Initializing flask app
app = Flask(__name__)
app.json.sort_keys = False

# Cross-Origin Resource Sharing
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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


# Route: Get all chargers
@app.route('/api/get_all_chargers', methods=['GET', 'POST'])
def fun_get_all_chargers():
    # if POST, should have email specified
    if request.method == 'POST':
        email = request.json['email']
        output = db_charger.get_all_chargers(input_email=email)
    # no email specified
    else:
        output = db_charger.get_all_chargers(input_email=None)

    if output['result'] == db_charger.CHARGER_NOT_FOUND:
        return {'success': False, 'api_response': db_charger.service_code_dict[output['result']]}

    return {'success': True, 'api_response': db_charger.service_code_dict[output['result']],
            'type': db_charger.service_code_dict[output['type']], 'content': output['content']}


# Route: Get favourite chargers
@app.route('/api/get_favourite_chargers', methods=['POST'])
def fun_get_favourite_chargers():
    email = request.json['email']

    output = db_charger.get_favourite_chargers(input_email=email)

    if output['result'] == db_charger.CHARGER_NOT_FOUND:
        return {'success': False, 'api_response': db_charger.service_code_dict[output['result']]}

    return {'success': True, 'api_response': db_charger.service_code_dict[output['result']], 'content': output['content']}


# Route: Modify favourite charger (add/remove)
@app.route('/api/modify_favourite_charger', methods=['POST'])
def fun_modify_favourite_chargers():
    email = request.json['email']
    charger_id = request.json['charger_id']
    action = request.json['action']

    output = db_favourite_charger.modify_favourite_charger(
        input_email=email, input_charger_id=charger_id, input_action=action)

    if output['result'] != db_favourite_charger.MODIFY_SUCCESS:
        return {'success': False, 'api_response': db_favourite_charger.service_code_dict[output['result']]}

    return {'success': True, 'api_response': db_favourite_charger.service_code_dict[output['result']]}


# Route: Get available connector details
@app.route('/api/get_all_connectors', methods=['GET'])
def get_connectors():
    output = db_connector_type.get_all_connectors()

    if output['result'] != db_connector_type.CONNECTOR_FOUND:
        return {'success': False, 'api_response': db_connector_type.service_code_dict[output['result']]}

    return {'success': True, 'api_response': db_connector_type.service_code_dict[output['result']], 'content': output['content']}


# Route: Add new vehicle
@app.route('/api/add_vehicle', methods=['POST'])
def fun_add_vehicle():
    email = request.json['email']
    vehicle_name = request.json['vehicle_name']
    vehicle_model = request.json['vehicle_model']
    vehicle_sn = request.json['vehicle_sn']
    vehicle_connector = request.json['vehicle_connector']

    output = db_vehicle.add_vehicle(
        input_email=email, input_vehicle_name=vehicle_name, input_vehicle_model=vehicle_model, input_vehicle_sn=vehicle_sn, input_vehicle_connector=vehicle_connector)

    if output['result'] == db_vehicle.ADD_FAILURE:
        return {'success': False, 'api_response': db_vehicle.service_code_dict[output['result']],
                'reason': helper_functions.join_strings(output['reason'], db_vehicle.service_code_dict)}

    return {'success': True, 'api_response': db_vehicle.service_code_dict[output['result']]}


# Running app
if __name__ == '__main__':
    app.run(debug=True)
