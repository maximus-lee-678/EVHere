import db_access.support_files.db_methods as db_methods
from flask_routes.flask_charge_current import flask_charge_current
from flask_routes.flask_charge_history import flask_charge_history
from flask_routes.flask_charger_available_connector import flask_charger_available_connector
from flask_routes.flask_charger_pv_historic import flask_charger_pv_historic
from flask_routes.flask_charger_rate_historic import flask_charger_rate_historic
from flask_routes.flask_charger import flask_charger
from flask_routes.flask_connector_type import flask_connector_type
from flask_routes.flask_favourite_charger import flask_favourite_charger
from flask_routes.flask_user_info import flask_user_info
from flask_routes.flask_vehicle import flask_vehicle

from flask import Flask
from flask_cors import CORS
import os

# if running sphinx, need to change directory to 'root'
current_working_directory_highest = os.path.basename(os.getcwd())
if current_working_directory_highest != 'team_15_flask_react':
    os.chdir('../')

# If db file not exists, create

if not os.path.exists(db_methods.DATABASE_PATH):
    print(f"[!] database not found!, creating new database... (this may take a while, wait for completion message!)")
    db_methods.touch_database()
    print(f"[i] created new database at {db_methods.DATABASE_PATH}!")

# Initializing flask app
app = Flask(__name__)

# Registering paths
app.register_blueprint(flask_charge_current)
app.register_blueprint(flask_charge_history)
app.register_blueprint(flask_charger_available_connector)
app.register_blueprint(flask_charger_pv_historic)
app.register_blueprint(flask_charger_rate_historic)
app.register_blueprint(flask_charger)
app.register_blueprint(flask_connector_type)
app.register_blueprint(flask_favourite_charger)
app.register_blueprint(flask_user_info)
app.register_blueprint(flask_vehicle)

# Flask settings
app.json.sort_keys = False

# Cross-Origin Resource Sharing
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# TODO
# loop thru current charges and update power consumption based on connector out

# Running app, allow '0.0.0.0' for all device access
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
