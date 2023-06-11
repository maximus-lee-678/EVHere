from flask import Blueprint, request

import flask_routes.flask_helper_functions as flask_helper_functions
import db_access.db_connector_type as db_connector_type

flask_connector_type = Blueprint('flask_connector_type', __name__, template_folder='flask_routes')

# Route: Get available connector details
@flask_connector_type.route('/api/get_all_connectors', methods=['GET'])
def get_connectors():
    output = db_connector_type.get_all_connectors()

    if output['result'] != db_connector_type.CONNECTOR_FOUND:
        return {'success': False, 'api_response': db_connector_type.service_code_dict[output['result']]}

    return {'success': True, 'api_response': db_connector_type.service_code_dict[output['result']], 'content': output['content']}