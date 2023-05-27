# Import flask and datetime module for showing date and time
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

import db_user_info
import db_methods
import db_charger

# If db file not exists, create
if not os.path.exists(db_methods.DATABASE_PATH):
    db_methods.touch_database()
    print(
        f"[!] database not found, created new database at {db_methods.DATABASE_PATH}!")

# Initializing flask app
app = Flask(__name__)
app.json.sort_keys = False

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/login', methods=['POST'])  # Route: Authenticate user login
def fun_login():
    email = request.json['email']
    password = request.json['password']

    return_code = db_user_info.login_user(email, password)
    return jsonify(result=return_code == db_user_info.LOGIN_SUCCESS, description=db_user_info.service_code_dict[return_code])


# Route: Create new user account
@app.route('/api/create_account', methods=['POST'])
def fun_create_account():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    full_name = request.json['full_name']
    phone_number = request.json['phone_number']

    return_code = db_user_info.create_user(
        username, password, email, full_name, phone_number)
    return jsonify(result=return_code == db_user_info.CREATE_SUCCESS, description=db_user_info.service_code_dict[return_code])


# Route: Get all chargers
@app.route('/api/get_all_chargers', methods=['GET', 'POST'])
def fun_get_chargers():
    list = []

    if request.method == 'POST':
        email = request.json['email']
        rows = db_charger.get_all_chargers(input_email=email)

        for row in rows:
            list.append({"id": row[0], "name": row[1],
                        "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                         "connectors": row[6], "online": row[7], "kilowatts": row[8], 
                         "twenty_four_hours": row[9], "last_updated": row[10], "is_favourite": row[11]})
    else:
        rows = db_charger.get_all_chargers(input_email=None)

        for row in rows:
            list.append({"id": row[0], "name": row[1],
                        "latitude": row[2], "longitude": row[3], "address": row[4], "provider": row[5],
                         "connectors": row[6], "online": row[7], "kilowatts": row[8], 
                         "twenty_four_hours": row[9], "last_updated": row[10]})

    return list


# Running app
if __name__ == '__main__':
    app.run(debug=True)
