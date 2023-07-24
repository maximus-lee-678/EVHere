import db_access.support_files.db_service_code_master as db_service_code_master

error_scenarios = [db_service_code_master.CONFIGURATION_ERROR,
                   db_service_code_master.INTERNAL_ERROR]


def format_for_endpoint(db_dictionary, success_scenarios_array):
    """
    | Takes a db dict and returns a formatted dict for delivery to endpoint.
    | **[Statuses]**
    | Error: When 'result' contains a value in flask_helper_functions.error_scenarios.
    | Success: When 'result' contains a value in success_scenarios_array.
    | Failure: When 'result' does not contain a value in success_scenarios_array.\n

    :returns: Dictionary
    :key 'status': (string) API_SUCCESS_STRING, API_FAILURE_STRING, API_ERROR_STRING.
    :key 'message': (string) response's corresponding 'result' string.
    :key 'reason': (array, one/multiple) *('status' == API_FAILURE_STRING)* reason for failure.
    :key 'data': (any) *('status' == API_SUCCESS_STRING)* response's 'content' OR None.
    """

    if db_dictionary['result'] in error_scenarios:
        return {
            'status': db_service_code_master.API_ERROR_STRING,
            'message': db_service_code_master.service_code_dict[db_dictionary['result']]
        }

    if db_dictionary['result'] in success_scenarios_array:
        return_dict = {
            'status': db_service_code_master.API_SUCCESS_STRING,
            'message': db_service_code_master.service_code_dict[db_dictionary['result']]
        }
        if 'content' in db_dictionary:
            return_dict.update({'data': db_dictionary['content']})
        else:
            return_dict.update({'data': None})
        return return_dict

    return {
        'status': db_service_code_master.API_FAILURE_STRING,
        'message': db_service_code_master.service_code_dict[db_dictionary['result']],
        'reason': [db_service_code_master.service_code_dict[i] for i in db_dictionary['reason']]
    }
