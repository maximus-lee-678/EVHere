def join_strings(service_code_array, service_code_dict):
    """
    Takes an array containing service codes and a service code dictionary and returns a
    space joined string containing decoded service codes.
    """
    service_code_decoded = []
    [service_code_decoded.append(service_code_dict[i])
     for i in service_code_array]

    return ' '.join(service_code_decoded)
