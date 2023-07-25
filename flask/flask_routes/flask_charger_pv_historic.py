from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_charger_pv_historic as db_charger_pv_historic

# Other db_access imports
# 


flask_charger_pv_historic = Blueprint(
    'db_charger_pv_historic', __name__, template_folder='flask_routes')
