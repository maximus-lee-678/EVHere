import db_access.support_files.db_service_code_master as db_service_code_master

error_scenarios = [db_service_code_master.CONFIGURATION_ERROR,
                   db_service_code_master.INTERNAL_ERROR
                   ]


def format_for_endpoint(db_dictionary, success_scenarios_array):
    """
    Takes a db dict and returns a formatted dict for delivery to endpoint.\n
    Returns Dictionary with keys:\n
    <status> API_SUCCESS_STRING, API_FAILURE_STRING or API_ERROR_STRING.
    \tError: When 'result' contains a value in flask_helper_functions.error_scenarios.
    \tSuccess: When 'result' contains a value in success_scenarios_array.
    \tFailure: When 'result' does not contain a value in success_scenarios_array.\n
    <message> 'result''s associated value.\n
    <reason> (if <status> is API_FAILURE_STRING) [Array] Reason for failure.\n
    <data> (if <status> is API_SUCCESS_STRING) [Array] 'content' OR None.
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


def join_strings(service_code_array, service_code_dict):
    """
    Takes an array containing service codes and a service code dictionary and returns a
    space joined string containing decoded service codes.
    """
    service_code_decoded = []
    [service_code_decoded.append(service_code_dict[i])
     for i in service_code_array]

    return ' '.join(service_code_decoded)
