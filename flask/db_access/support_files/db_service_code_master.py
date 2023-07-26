"""
| This file holds all status codes and their corresponding meanings.
| This should be included in all functional db files.

| Each table gets a block of 100. 
| First 5 values are reserved for database interaction operations. (these are currently not used)
| Details(errors, extra info, etc.) should count up and completion codes should count down.
| (e.g. reserved: 0-4 | error: 5,6,7,... | completion: 100,99,98,...)
| ALL ASSIGNMENTS MUST BE DIFFERENT VALUES!

| *"What is this abomination?!"*
| *"Like the good old days of C, eh?"*
"""

API_SUCCESS_STRING = 'success'
API_FAILURE_STRING = 'fail'
API_ERROR_STRING = 'error'


def ez_update(code, code_def):
    service_code_dict.update({code: code_def})


service_code_dict = {}

# generic [0-99]
TYPE_GENERIC = 0
ez_update(TYPE_GENERIC, "This is a generic operation.")

HASHMAP_GENERIC_SUCCESS = 1
ez_update(HASHMAP_GENERIC_SUCCESS, "Hashmap assembled.")

HASHMAP_GENERIC_EMPTY = 2
ez_update(HASHMAP_GENERIC_EMPTY, "Hashmap returned empty.")

SELECT_GENERIC_SUCCESS = 3
ez_update(SELECT_GENERIC_SUCCESS, "Select succeeded.")

SELECT_GENERIC_EMPTY = 4
ez_update(SELECT_GENERIC_EMPTY, "Select returned empty.")
# >
# >
OPERATION_OK = 5
ez_update(OPERATION_OK, "Operation Succeeded.")

MISSING_FIELDS = 6
ez_update(MISSING_FIELDS, "One or more json fields are missing.")

CONFIGURATION_ERROR = 7
ez_update(CONFIGURATION_ERROR, "Function not configured properly.")

INTERNAL_ERROR = 8  # oh damn better call the programmers
ez_update(INTERNAL_ERROR, "Something went wrong.")

BAD_REQUEST = 9
ez_update(BAD_REQUEST, "The server will not process the request due to something that is perceived to be a client error.")

#########################

# user_info [100-199]
TYPE_USER_INFO = 100
ez_update(TYPE_USER_INFO, "This is a user info operation.")

HASHMAP_USER_INFO_SUCCESS = 101
ez_update(HASHMAP_USER_INFO_SUCCESS, "User info hashmap assembled.")

HASHMAP_USER_INFO_EMPTY = 102
ez_update(HASHMAP_USER_INFO_EMPTY, "User info hashmap returned empty.")

SELECT_USER_INFO_SUCCESS = 103
ez_update(SELECT_USER_INFO_SUCCESS, "User info select succeeded.")

SELECT_USER_INFO_EMPTY = 104
ez_update(SELECT_USER_INFO_EMPTY, "User info select returned empty.")
# >
# >
USERNAME_INVALID_LENGTH = 105
ez_update(USERNAME_INVALID_LENGTH, "Username field contains string of invalid length.")

PASSWORD_INVALID_LENGTH = 106
ez_update(PASSWORD_INVALID_LENGTH, "Password field contains string of invalid length.")

PASSWORD_INVALID_SYNTAX = 107
ez_update(PASSWORD_INVALID_SYNTAX, "Password field contains string of invalid syntax.")

EMAIL_INVALID_LENGTH = 108
ez_update(EMAIL_INVALID_LENGTH, "Email field contains string of invalid length.")

EMAIL_INVALID_SYNTAX = 109
ez_update(EMAIL_INVALID_SYNTAX, "Email field contains string of invalid syntax.")

ACCOUNT_ALREADY_EXISTS = 110
ez_update(ACCOUNT_ALREADY_EXISTS, "An account with the same email already exists.")

PHONE_NUMBER_INVALID = 111
ez_update(PHONE_NUMBER_INVALID, "Phone number field contains string of invalid syntax.")

FULL_NAME_INVALID_LENGTH = 112
ez_update(FULL_NAME_INVALID_LENGTH, "Full name field contains string of invalid length.")

EMAIL_PASSWORD_INVALID = 113
ez_update(EMAIL_PASSWORD_INVALID, "Email or Password is incorrect.")
# >
# >
USER_INFO_CREATE_SUCCESS = 199
ez_update(USER_INFO_CREATE_SUCCESS, "Account created.")

USER_INFO_CREATE_FAILURE = 198
ez_update(USER_INFO_CREATE_FAILURE, "Account not created.")

LOGIN_SUCCESS = 197
ez_update(LOGIN_SUCCESS, "Logged in.")

LOGIN_FAILURE = 196
ez_update(LOGIN_FAILURE, "Could not log in.")

ACCOUNT_FOUND = 195
ez_update(ACCOUNT_FOUND, "Matching account found.")

ACCOUNT_NOT_FOUND = 194
ez_update(ACCOUNT_NOT_FOUND, "No matching account found.")

USER_INFO_VALID = 193
ez_update(USER_INFO_VALID, "Provided user info is valid.")

USER_INFO_INVALID = 192
ez_update(USER_INFO_INVALID, "Provided user info is invalid.")

USER_INFO_UPDATE_SUCCESS = 191
ez_update(USER_INFO_UPDATE_SUCCESS, "Account details updated.")

USER_INFO_UPDATE_FAILURE = 190
ez_update(USER_INFO_UPDATE_FAILURE, "Account details not updated.")

#########################

# charger [200-299]
TYPE_CHARGER = 200
ez_update(TYPE_CHARGER, "This is a charger operation.")

HASHMAP_CHARGER_SUCCESS = 201
ez_update(HASHMAP_CHARGER_SUCCESS, "Charger hashmap assembled.")

HASHMAP_CHARGER_EMPTY = 202
ez_update(HASHMAP_CHARGER_EMPTY, "Charger hashmap returned empty.")

SELECT_CHARGER_SUCCESS = 203
ez_update(SELECT_CHARGER_SUCCESS, "Charger select succeeded.")

SELECT_CHARGER_EMPTY = 204
ez_update(SELECT_CHARGER_EMPTY, "Charger select returned empty.")
# >
# >
#
# >
# >
CHARGER_FOUND = 299
ez_update(CHARGER_FOUND, "Chargers found.")

CHARGER_NOT_FOUND = 298
ez_update(CHARGER_NOT_FOUND, "Chargers not found.")

CHARGER_UPDATE_SUCCESS = 297
ez_update(CHARGER_UPDATE_SUCCESS, "Charger details updated.")

CHARGER_UPDATE_FAILURE = 296
ez_update(CHARGER_UPDATE_FAILURE, "Chargers details could not be updated.")

#########################

# charger_available_connector [300-399]
TYPE_CHARGER_AVAILABLE_CONNECTOR = 300
ez_update(TYPE_CHARGER_AVAILABLE_CONNECTOR, "This is a charger available connector operation.")

HASHMAP_CHARGER_AVAILABLE_CONNECTOR_SUCCESS = 301
ez_update(HASHMAP_CHARGER_AVAILABLE_CONNECTOR_SUCCESS, "Charger available connector hashmap assembled.")

HASHMAP_CHARGER_AVAILABLE_CONNECTOR_EMPTY = 302
ez_update(HASHMAP_CHARGER_AVAILABLE_CONNECTOR_EMPTY, "Charger available connector hashmap returned empty.")

SELECT_CHARGER_AVAILABLE_CONNECTOR_SUCCESS = 303
ez_update(SELECT_CHARGER_AVAILABLE_CONNECTOR_SUCCESS, "Charger available connector select succeeded.")

SELECT_CHARGER_AVAILABLE_CONNECTOR_EMPTY = 304
ez_update(SELECT_CHARGER_AVAILABLE_CONNECTOR_EMPTY, "Charger available connector select returned empty.")
# >
# >
CHARGER_AVAILABLE_CONNECTOR_INVALID_ENERGY_LEVEL = 305
ez_update(CHARGER_AVAILABLE_CONNECTOR_INVALID_ENERGY_LEVEL, "Invalid energy level specified.")
# >
# >
AVAILABLE_CONNECTORS_NOT_FOUND = 399
ez_update(AVAILABLE_CONNECTORS_NOT_FOUND, "Charger connector types found.")

AVAILABLE_CONNECTORS_FOUND = 398
ez_update(AVAILABLE_CONNECTORS_FOUND, "Charger connector types not found.")

AVAILABLE_CONNECTOR_IN_USE = 397
ez_update(AVAILABLE_CONNECTOR_IN_USE, "This charger connector is in use.")

AVAILABLE_CONNECTOR_NOT_IN_USE = 396
ez_update(AVAILABLE_CONNECTOR_NOT_IN_USE, "This charger connector is not in use.")

AVAILABLE_CONNECTOR_SET_USE_STATE_SUCCESS = 395
ez_update(AVAILABLE_CONNECTOR_NOT_IN_USE, "Charger connector use state changed.")

#########################

# connector_type [400-499]
TYPE_CONNECTOR_TYPE = 400
ez_update(TYPE_CONNECTOR_TYPE, "This is a connector type operation.")

HASHMAP_CONNECTOR_TYPE_SUCCESS = 401
ez_update(HASHMAP_CONNECTOR_TYPE_SUCCESS, "Connector type hashmap assembled.")

HASHMAP_CONNECTOR_TYPE_EMPTY = 402
ez_update(HASHMAP_CONNECTOR_TYPE_EMPTY, "Connector type hashmap returned empty.")

SELECT_CONNECTOR_TYPE_SUCCESS = 403
ez_update(SELECT_CONNECTOR_TYPE_SUCCESS, "Connector type select succeeded.")

SELECT_CONNECTOR_TYPE_EMPTY = 404  # poetic
ez_update(SELECT_CONNECTOR_TYPE_EMPTY, "Connector type select returned empty.")
# >
# >
#
# >
# >
CONNECTOR_FOUND = 499
ez_update(CONNECTOR_FOUND, "Connector type definitions found.")

CONNECTOR_NOT_FOUND = 498
ez_update(CONNECTOR_NOT_FOUND, "Connector type definitions not found.")

#########################

# favourited_chargers [500-599]
TYPE_FAVOURITED_CHARGERS = 500
ez_update(TYPE_FAVOURITED_CHARGERS, "This is a favourited chargers operation.")

HASHMAP_FAVOURITED_CHARGERS_SUCCESS = 501
ez_update(HASHMAP_FAVOURITED_CHARGERS_SUCCESS, "Favourited chargers hashmap assembled.")

HASHMAP_FAVOURITED_CHARGERS_EMPTY = 502
ez_update(HASHMAP_FAVOURITED_CHARGERS_EMPTY, "Favourited chargers hashmap returned empty.")

SELECT_FAVOURITED_CHARGERS_SUCCESS = 503
ez_update(SELECT_FAVOURITED_CHARGERS_SUCCESS, "Favourited chargers select succeeded.")

SELECT_FAVOURITED_CHARGERS_EMPTY = 504
ez_update(SELECT_FAVOURITED_CHARGERS_EMPTY, "Favourited chargers select returned empty.")
# >
# >
FAVOURITE_CHARGER_MODIFY_ILLEGAL_OPERATION = 505
ez_update(FAVOURITE_CHARGER_MODIFY_ILLEGAL_OPERATION, "Illegal favourite modify favourite operation specified.")

FAVOURITE_CHARGER_MODIFY_INVALID_OPERATION = 506
ez_update(FAVOURITE_CHARGER_MODIFY_INVALID_OPERATION, "Invalid favourite modify favourite operation specified.")

FAVOURITE_CHARGER_DUPLICATE_ENTRY = 507
ez_update(FAVOURITE_CHARGER_DUPLICATE_ENTRY, "A similar favourite charger already exists.")
# >
# >
FAVOURITE_CHARGERS_NOT_FOUND = 599
ez_update(FAVOURITE_CHARGERS_NOT_FOUND, "No favourite chargers found.")

FAVOURITE_CHARGERS_FOUND = 598
ez_update(FAVOURITE_CHARGERS_FOUND, "Favourite chargers found.")

FAVOURITE_CHARGER_MODIFY_SUCCESS = 597
ez_update(FAVOURITE_CHARGER_MODIFY_SUCCESS, "Favourite charger modified.")

FAVOURITE_CHARGER_MODIFY_FAILURE = 596
ez_update(FAVOURITE_CHARGER_MODIFY_FAILURE, "Favourite charger could not be modified.")

#########################

# vehicle_info [600-699]
TYPE_VEHICLE_INFO = 600
ez_update(TYPE_VEHICLE_INFO, "This is a vehicle info operation.")

HASHMAP_VEHICLE_INFO_SUCCESS = 601
ez_update(HASHMAP_VEHICLE_INFO_SUCCESS, "Vehicle info hashmap assembled.")

HASHMAP_VEHICLE_INFO_EMPTY = 602
ez_update(HASHMAP_VEHICLE_INFO_EMPTY, "Vehicle info hashmap returned empty.")

SELECT_VEHICLE_INFO_SUCCESS = 603
ez_update(SELECT_VEHICLE_INFO_SUCCESS, "Vehicle info select succeeded.")

SELECT_VEHICLE_INFO_EMPTY = 604
ez_update(SELECT_VEHICLE_INFO_EMPTY, "Vehicle info select returned empty.")
# >
# >
VEHICLE_NAME_INVALID_LENGTH = 605
ez_update(VEHICLE_NAME_INVALID_LENGTH, "Vehicle name field contains string of invalid length.")

VEHICLE_MODEL_INVALID_LENGTH = 606
ez_update(VEHICLE_MODEL_INVALID_LENGTH, "Vehicle model field contains string of invalid length.")

VEHICLE_SN_INVALID_LENGTH = 607
ez_update(VEHICLE_SN_INVALID_LENGTH, "Vehicle SN field contains string of invalid length.")
# >
# >
VEHICLE_ADD_SUCCESS = 699
ez_update(VEHICLE_ADD_SUCCESS, "Vehicle added.")

VEHICLE_ADD_FAILURE = 698
ez_update(VEHICLE_ADD_FAILURE, "Vehicle could not be added.")

VEHICLE_REMOVE_SUCCESS = 697
ez_update(VEHICLE_REMOVE_SUCCESS, "Vehicle removed.")

VEHICLE_REMOVE_FAILURE = 696
ez_update(VEHICLE_REMOVE_FAILURE, "Vehicle could not be removed.")

VEHICLE_FOUND = 695
ez_update(VEHICLE_FOUND, "Vehicle information found.")

VEHICLE_NOT_FOUND = 694
ez_update(VEHICLE_NOT_FOUND, "Vehicle information could not be found.")

#########################

# charge_history [700-799]
TYPE_CHARGE_HISTORY = 700
ez_update(TYPE_CHARGE_HISTORY, "This is a charge history operation.")

HASHMAP_CHARGE_HISTORY_SUCCESS = 701
ez_update(HASHMAP_CHARGE_HISTORY_SUCCESS, "Charge history hashmap assembled.")

HASHMAP_CHARGE_HISTORY_EMPTY = 702
ez_update(HASHMAP_CHARGE_HISTORY_EMPTY, "Charge history hashmap returned empty.")

SELECT_CHARGE_HISTORY_SUCCESS = 703
ez_update(SELECT_CHARGE_HISTORY_SUCCESS, "Charge history select succeeded.")

SELECT_CHARGE_HISTORY_EMPTY = 704
ez_update(SELECT_CHARGE_HISTORY_EMPTY, "Charge history select returned empty.")
# >
# >
CHARGE_HISTORY_INVALID_CHARGE_LEVEL = 705
ez_update(CHARGE_HISTORY_INVALID_CHARGE_LEVEL, "Invalid battery percentage specified.")

CHARGE_HISTORY_ALREADY_CHARGING = 706
ez_update(CHARGE_HISTORY_ALREADY_CHARGING, "Can't start a new charge while already charging.")

CHARGE_HISTORY_NOT_CHARGING = 707
ez_update(CHARGE_HISTORY_NOT_CHARGING, "Can't finish a charge, this user does not have an unfinished entry.")
# >
# >
CHARGE_HISTORY_CREATE_SUCCESS = 799
ez_update(CHARGE_HISTORY_CREATE_SUCCESS, "Charge history updated - started.")

CHARGE_HISTORY_CREATE_FAILURE = 798
ez_update(CHARGE_HISTORY_CREATE_FAILURE, "Charge history could not be created.")

CHARGE_HISTORY_FINISH_FAILURE = 797
ez_update(CHARGE_HISTORY_FINISH_FAILURE, "Charge history could not be finished.")

CHARGE_HISTORY_FINISH_SUCCESS = 796
ez_update(CHARGE_HISTORY_FINISH_SUCCESS, "Charge history updated - finished.")

CHARGE_HISTORY_FOUND = 795
ez_update(CHARGE_HISTORY_FOUND, "Charge history found.")

CHARGE_HISTORY_NOT_FOUND = 794
ez_update(CHARGE_HISTORY_NOT_FOUND, "Charge history not found.")

#########################

# charge_current [800-899]
TYPE_CHARGE_CURRENT = 800
ez_update(TYPE_CHARGE_CURRENT, "This is a charge current operation.")

HASHMAP_CHARGE_CURRENT_SUCCESS = 801
ez_update(HASHMAP_CHARGE_CURRENT_SUCCESS, "Charge current hashmap assembled.")

HASHMAP_CHARGE_CURRENT_EMPTY = 802
ez_update(HASHMAP_CHARGE_CURRENT_EMPTY, "Charge current hashmap returned empty.")

SELECT_CHARGE_CURRENT_SUCCESS = 803
ez_update(SELECT_CHARGE_CURRENT_SUCCESS, "Charge current select succeeded.")

SELECT_CHARGE_CURRENT_EMPTY = 804
ez_update(SELECT_CHARGE_CURRENT_EMPTY, "Charge current select returned empty.")
# >
# >
CURRENCY_INVALID = 805
ez_update(CURRENCY_INVALID, "Currency field contains string of invalid syntax.")
# >
# >
CHARGE_CURRENT_CREATE_SUCCESS = 899
ez_update(CHARGE_CURRENT_CREATE_SUCCESS, "Charge current created.")

CHARGE_CURRENT_CREATE_FAILURE = 898
ez_update(CHARGE_CURRENT_CREATE_FAILURE, "Charge current could not be created.")

CHARGE_CURRENT_REMOVE_SUCCESS = 897
ez_update(CHARGE_CURRENT_REMOVE_SUCCESS, "Charge current removed.")

CHARGE_CURRENT_REMOVE_FAILURE = 896
ez_update(CHARGE_CURRENT_REMOVE_FAILURE, "Charge current could not be removed.")

CHARGE_CURRENT_NOT_FOUND = 895
ez_update(CHARGE_CURRENT_NOT_FOUND, "Charge current entry not found.")

CHARGE_CURRENT_FOUND = 894
ez_update(CHARGE_CURRENT_FOUND, "Charge current entry found.")

CHARGE_CURRENT_UPDATE_SUCCESS = 893
ez_update(CHARGE_CURRENT_UPDATE_SUCCESS, "Charge current entry updated.")

CHARGE_CURRENT_UPDATE_FAILURE = 892
ez_update(CHARGE_CURRENT_UPDATE_FAILURE, "Charge current entry could not be updated.")

#########################

# charger_pv_historic [900-999]
TYPE_CHARGER_PV_HISTORIC = 900
ez_update(TYPE_CHARGER_PV_HISTORIC, "This is a charger PV historic operation.")

HASHMAP_CHARGER_PV_HISTORIC_SUCCESS = 901
ez_update(HASHMAP_CHARGER_PV_HISTORIC_SUCCESS, "Charger PV historic hashmap assembled.")

HASHMAP_CHARGER_PV_HISTORIC_EMPTY = 902
ez_update(HASHMAP_CHARGER_PV_HISTORIC_EMPTY, "Charger PV historic hashmap returned empty.")

SELECT_CHARGER_PV_HISTORIC_SUCCESS = 903
ez_update(SELECT_CHARGER_PV_HISTORIC_SUCCESS, "Charger PV historic select succeeded.")

SELECT_CHARGER_PV_HISTORIC_EMPTY = 904
ez_update(SELECT_CHARGER_PV_HISTORIC_EMPTY, "Charger PV historic select returned empty.")
# >
# >
#
# >
# >
#

#########################

# charger_rate_historic [1000-1999]
TYPE_CHARGER_RATE_HISTORIC = 1000
ez_update(TYPE_CHARGER_RATE_HISTORIC, "This is a charger rate historic operation.")

HASHMAP_CHARGER_RATE_HISTORIC_SUCCESS = 1001
ez_update(HASHMAP_CHARGER_RATE_HISTORIC_SUCCESS, "Charger rate historic hashmap assembled.")

HASHMAP_CHARGER_RATE_HISTORIC_EMPTY = 1002
ez_update(HASHMAP_CHARGER_RATE_HISTORIC_EMPTY, "Charger rate historic hashmap returned empty.")

SELECT_CHARGER_RATE_HISTORIC_SUCCESS = 1003
ez_update(SELECT_CHARGER_RATE_HISTORIC_SUCCESS, "Charger rate historic select succeeded.")

SELECT_CHARGER_RATE_HISTORIC_EMPTY = 1004
ez_update(SELECT_CHARGER_RATE_HISTORIC_EMPTY, "Charger rate historic select returned empty.")
# >
# >
#
# >
# >
CHARGER_RATE_HISTORIC_FOUND = 1099
ez_update(CHARGER_RATE_HISTORIC_FOUND, "Charger rate historic found.")

CHARGER_RATE_HISTORIC_NOT_FOUND = 1098
ez_update(CHARGER_RATE_HISTORIC_NOT_FOUND, "Charger rate historic not found.")

#########################

# converts generic messages into detailed ones based on generic message type and specified convert-to type
translations = {
    HASHMAP_GENERIC_SUCCESS: {
        TYPE_USER_INFO: HASHMAP_USER_INFO_SUCCESS,
        TYPE_CHARGER: HASHMAP_CHARGER_SUCCESS,
        TYPE_CHARGER_AVAILABLE_CONNECTOR: HASHMAP_CHARGER_AVAILABLE_CONNECTOR_SUCCESS,
        TYPE_CONNECTOR_TYPE: HASHMAP_CONNECTOR_TYPE_SUCCESS,
        TYPE_FAVOURITED_CHARGERS: HASHMAP_FAVOURITED_CHARGERS_SUCCESS,
        TYPE_VEHICLE_INFO: HASHMAP_VEHICLE_INFO_SUCCESS,
        TYPE_CHARGE_HISTORY: HASHMAP_CHARGE_HISTORY_SUCCESS,
        TYPE_CHARGE_CURRENT: HASHMAP_CHARGE_CURRENT_SUCCESS,
        TYPE_CHARGER_PV_HISTORIC: HASHMAP_CHARGER_PV_HISTORIC_SUCCESS,
        TYPE_CHARGER_RATE_HISTORIC: HASHMAP_CHARGER_RATE_HISTORIC_SUCCESS
    },
    HASHMAP_GENERIC_EMPTY: {
        TYPE_USER_INFO: HASHMAP_USER_INFO_EMPTY,
        TYPE_CHARGER: HASHMAP_CHARGER_EMPTY,
        TYPE_CHARGER_AVAILABLE_CONNECTOR: HASHMAP_CHARGER_AVAILABLE_CONNECTOR_EMPTY,
        TYPE_CONNECTOR_TYPE: HASHMAP_CONNECTOR_TYPE_EMPTY,
        TYPE_FAVOURITED_CHARGERS: HASHMAP_FAVOURITED_CHARGERS_EMPTY,
        TYPE_VEHICLE_INFO: HASHMAP_VEHICLE_INFO_EMPTY,
        TYPE_CHARGE_HISTORY: HASHMAP_CHARGE_HISTORY_EMPTY,
        TYPE_CHARGE_CURRENT: HASHMAP_CHARGE_CURRENT_EMPTY,
        TYPE_CHARGER_PV_HISTORIC: HASHMAP_CHARGER_PV_HISTORIC_EMPTY,
        TYPE_CHARGER_RATE_HISTORIC: HASHMAP_CHARGER_RATE_HISTORIC_EMPTY
    },
    SELECT_GENERIC_SUCCESS: {
        TYPE_USER_INFO: SELECT_USER_INFO_SUCCESS,
        TYPE_CHARGER: SELECT_CHARGER_SUCCESS,
        TYPE_CHARGER_AVAILABLE_CONNECTOR: SELECT_CHARGER_AVAILABLE_CONNECTOR_SUCCESS,
        TYPE_CONNECTOR_TYPE: SELECT_CONNECTOR_TYPE_SUCCESS,
        TYPE_FAVOURITED_CHARGERS: SELECT_FAVOURITED_CHARGERS_SUCCESS,
        TYPE_VEHICLE_INFO: SELECT_VEHICLE_INFO_SUCCESS,
        TYPE_CHARGE_HISTORY: SELECT_CHARGE_HISTORY_SUCCESS,
        TYPE_CHARGE_CURRENT: SELECT_CHARGE_CURRENT_SUCCESS,
        TYPE_CHARGER_PV_HISTORIC: SELECT_CHARGER_PV_HISTORIC_SUCCESS,
        TYPE_CHARGER_RATE_HISTORIC: SELECT_CHARGER_RATE_HISTORIC_SUCCESS
    },
    SELECT_GENERIC_EMPTY: {
        TYPE_USER_INFO: SELECT_USER_INFO_EMPTY,
        TYPE_CHARGER: SELECT_CHARGER_EMPTY,
        TYPE_CHARGER_AVAILABLE_CONNECTOR: SELECT_CHARGER_AVAILABLE_CONNECTOR_EMPTY,
        TYPE_CONNECTOR_TYPE: SELECT_CONNECTOR_TYPE_EMPTY,
        TYPE_FAVOURITED_CHARGERS: SELECT_FAVOURITED_CHARGERS_EMPTY,
        TYPE_VEHICLE_INFO: SELECT_VEHICLE_INFO_EMPTY,
        TYPE_CHARGE_HISTORY: SELECT_CHARGE_HISTORY_EMPTY,
        TYPE_CHARGE_CURRENT: SELECT_CHARGE_CURRENT_EMPTY,
        TYPE_CHARGER_PV_HISTORIC: SELECT_CHARGER_PV_HISTORIC_EMPTY,
        TYPE_CHARGER_RATE_HISTORIC: SELECT_CHARGER_RATE_HISTORIC_EMPTY
    }
}
