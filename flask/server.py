"""
API endpoints ALWAYS follow this format:\n
[status] success, fail, error
\tsuccess: very good, contains [content] (nullable)
\tfail: could not finish request, [reason] will be given
\terror: server blew up
[message] always included, request outcome.
[content] when [status==success] (nullable)
[reason] when [status==fail], why it failed.
"""
from flask_routes.flask_charge_current import flask_charge_current
from flask_routes.flask_charge_history import flask_charge_history
from flask_routes.flask_vehicle import flask_vehicle
from flask_routes.flask_user_info import flask_user_info
from flask_routes.flask_favourite_charger import flask_favourite_charger
from flask_routes.flask_connector_type import flask_connector_type
from flask_routes.flask_charger import flask_charger
from flask import Flask
from flask_cors import CORS
import os

# If db file not exists, create
import db_access.support_files.db_methods as db_methods

if not os.path.exists(db_methods.DATABASE_PATH):
    db_methods.touch_database()
    print(
        f"[!] database not found, created new database at {db_methods.DATABASE_PATH}!")

# Initializing flask app
app = Flask(__name__)

# Registering paths
app.register_blueprint(flask_user_info)
app.register_blueprint(flask_charger)
app.register_blueprint(flask_connector_type)
app.register_blueprint(flask_favourite_charger)
app.register_blueprint(flask_vehicle)
app.register_blueprint(flask_charge_history)
app.register_blueprint(flask_charge_current)

# Flask settings
app.json.sort_keys = False

# Cross-Origin Resource Sharing
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# TODO
# loop thru current charges and update power consumption based on connector out

# Running app
if __name__ == '__main__':
    app.run(debug=True)
    