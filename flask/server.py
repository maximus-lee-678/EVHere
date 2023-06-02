# Import flask and datetime module for showing date and time
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

import db_user_info
import db_methods
import db_charger
import db_favourite_charger

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
        return {'result': db_user_info.service_code_dict[output['result']], 'reason': db_user_info.service_code_dict[output['reason']]}

    return {'result': db_user_info.service_code_dict[output['result']]}


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
        return {'result': db_user_info.service_code_dict[output['result']], 'reason': db_user_info.service_code_dict[output['reason']]}

    return {'result': db_user_info.service_code_dict[output['result']]}


# Route: Get all chargers
@app.route('/api/get_all_chargers', methods=['GET', 'POST'])
def fun_get_all_chargers():
    list = []

    # if POST, should have email specified, add is_favourite column
    if request.method == 'POST':
        email = request.json['email']
        output = db_charger.get_all_chargers(input_email=email)

        if output['result'] == db_charger.CHARGER_NOT_FOUND:
            return {'result': db_charger.service_code_dict[output['result']]}

        for row in output['content']:
            list.append({"id": row[0], "name": row[1],
                        "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                         "connectors": row[6], "online": row[7], "kilowatts": row[8],
                         "twenty_four_hours": row[9], "last_updated": row[10], "is_favourite": row[11]})
    # no email specified, no is_favourite
    else:
        output = db_charger.get_all_chargers(input_email=None)

        if output['result'] == db_charger.CHARGER_NOT_FOUND:
            return {'result': db_charger.service_code_dict[output['result']]}

        for row in output['content']:
            list.append({"id": row[0], "name": row[1],
                        "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                         "connectors": row[6], "online": row[7], "kilowatts": row[8],
                         "twenty_four_hours": row[9], "last_updated": row[10]})

    return {'result': db_charger.service_code_dict[output['result']], 'type': db_charger.service_code_dict[output['type']], 'content': list}


# Route: Get favourite chargers
@app.route('/api/get_favourite_chargers', methods=['POST'])
def fun_get_favourite_chargers():
    email = request.json['email']

    output = db_charger.get_favourite_chargers(input_email=email)

    if output['result'] != db_charger.CHARGER_FOUND:
        return {'result': db_charger.service_code_dict[output['result']]}

    list = []
    rows = output['content']

    for row in rows:
        list.append({"id": row[0], "name": row[1],
                    "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                     "connectors": row[6], "online": row[7], "kilowatts": row[8],
                     "twenty_four_hours": row[9], "last_updated": row[10]})

    return {'result': db_charger.service_code_dict[output['result']], 'content': list}


# Route: Modify favourite charger (add/remove)
@app.route('/api/modify_favourite_charger', methods=['POST'])
def fun_modify_favourite_chargers():
    email = request.json['email']
    charger_id = request.json['charger_id']
    action = request.json['action']

    output = db_favourite_charger.modify_favourite_charger(
        input_email=email, input_charger_id=charger_id, input_action=action)

    return {'result': db_favourite_charger.service_code_dict[output['result']]}


# Running app
if __name__ == '__main__':
    app.run(debug=True)
