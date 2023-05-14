# Import flask and datetime module for showing date and time
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import time
import json

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


# Route: Authenticate user login
@app.route('/login', methods=['POST'])
def fun_login():
    email = request.json['email']
    password = request.json['password']

    return_code = db_user_info.login_user(email, password)
    return jsonify(result=return_code == db_user_info.LOGIN_SUCCESS, description=db_user_info.service_code_dict[return_code])


# Route: Create new user account
@app.route('/create_account', methods=['POST'])
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
@app.route('/get_chargers')
def fun_get_chargers():
    rows = db_charger.get_chargers()

    list = []
    for row in rows:
        list.append({"name": row[0], "lat": row[1], "long": row[2]})

    return list

# Running app
if __name__ == '__main__':
    app.run(debug=True)
