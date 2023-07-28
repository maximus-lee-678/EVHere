from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_charger_rate_historic as db_charger_rate_historic

# Other db_access imports
# 


flask_charger_rate_historic = Blueprint('flask_charger_rate_historic', __name__, template_folder='flask_routes')


@flask_charger_rate_historic.route('/api/get_all_past_charger_rates', methods=['GET'])
def fun_get_all_past_charger_rates():
    '''
    | Endpoint implementation for <Route: Get all past charger rates>

    :request GET fields: id_charger

    :returns: Dictionary

    | **Refer to:**
    | :meth:`db_access.db_charger_rate_historic.get_all_past_charger_rates`
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    '''
    
    # retrieve charger actual
    id_charger = request.args.get('id_charger')

    charger_response = db_charger_rate_historic.get_all_past_charger_rates(id_charger)

    return flask_helper_functions.format_for_endpoint(db_dictionary=charger_response, 
                                                      success_scenarios_array=[db_service_code_master.CHARGER_RATE_HISTORIC_FOUND, 
                                                                               db_service_code_master.CHARGER_RATE_HISTORIC_NOT_FOUND])
