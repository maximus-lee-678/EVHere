# Import flask and datetime module for showing date and time
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os, time, json

import db_user_info, db_methods

# If db file not exists, create
if not os.path.exists(db_methods.DATABASE_PATH):
    db_methods.touch_database()
    print(f"[!] database not found, created new database at {db_methods.DATABASE_PATH}!")

# Initializing flask app
app = Flask(__name__)
app.json.sort_keys = False

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Route: Authenticate user login
@app.route('/login', methods=['POST'])      
def fun_login():
    username = request.json['username']
    password = request.json['password']
    return {'username': username, 'password': password}

# Route: Create new user account
@app.route('/create_account', methods=['POST'])      
def login_create_account():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    full_name = request.json['full_name']
    phone_number = request.json['phone_number']

    return_code = db_user_info.create_user(username, password, email, full_name, phone_number)
    return jsonify(result=return_code == 0, description=db_user_info.create_user_code_dict[return_code])

# Running app
if __name__ == '__main__':
    app.run(debug=True)