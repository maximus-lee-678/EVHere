from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
#

# Other db_access imports
#


flask_generic = Blueprint('flask_generic', __name__,
                          template_folder='flask_routes')


@flask_generic.route('/api/handshake', methods=['GET'])
def fun_get_all_chargers():
    """
    | Endpoint implementation for <Route: Check if server alive>


    :returns: Dictionary 

    | **Refer to:**
    | :meth:`flask_routes.flask_helper_functions.format_for_endpoint`
    """

    return flask_helper_functions.format_for_endpoint(db_dictionary={'result': db_service_code_master.OPERATION_OK},
                                                      success_scenarios_array=[db_service_code_master.OPERATION_OK])
