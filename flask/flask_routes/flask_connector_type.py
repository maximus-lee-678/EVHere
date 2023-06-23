from flask import Blueprint, request

# Universal imports
import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.support_files.db_service_code_master as db_service_code_master

# Core import
import db_access.db_connector_type as db_connector_type

# Other db_access imports
#


flask_connector_type = Blueprint(
    'flask_connector_type', __name__, template_folder='flask_routes')


# Route: Get available connector details
@flask_connector_type.route('/api/get_all_connectors', methods=['GET'])
def fun_get_connectors():
    # retrieve connector types actual
    connector_type_response = db_connector_type.get_all_connectors()

    return flask_helper_functions.format_for_endpoint(db_dictionary=connector_type_response,
                                                    success_scenarios_array=[db_service_code_master.CONNECTOR_FOUND])
