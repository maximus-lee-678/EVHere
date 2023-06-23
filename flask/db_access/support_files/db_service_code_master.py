"""
This file holds all status codes and their corresponding meanings.
This should be included in all functional db files.

Each table gets a block of 100. Details(errors, extra info, etc.) should count up and completion codes should count down.
(e.g. error: 1,2,3,... | completion: 100,99,98,...)
NO ASSIGNMENTS CAN HAVE THE SAME VALUE!

"What is this abomination?!"
"Like the good old days of C, eh?"
"""

def ez_update(code, code_def):
    service_code_dict.update({code: code_def})

service_code_dict = {}

# generic [0-99]
MISSING_FIELDS = 0
ez_update(MISSING_FIELDS, "One or more fields are missing.")

CONFIGURATION_ERROR = 1
ez_update(CONFIGURATION_ERROR, "Function not configured properly.")

INTERNAL_ERROR = 2  # oh damn better call the programmers
ez_update(INTERNAL_ERROR, "Something went wrong.")

# user_info [100-199]
USERNAME_INVALID_LENGTH = 100
ez_update(USERNAME_INVALID_LENGTH, "Username field contains string of invalid length.")

PASSWORD_INVALID_LENGTH = 101
ez_update(PASSWORD_INVALID_LENGTH, "Password field contains string of invalid length.")

PASSWORD_INVALID_SYNTAX = 102
ez_update(PASSWORD_INVALID_SYNTAX, "Password field contains string of invalid syntax.")

EMAIL_INVALID_LENGTH = 103
ez_update(EMAIL_INVALID_LENGTH, "Email field contains string of invalid length.")

EMAIL_INVALID_SYNTAX = 104
ez_update(EMAIL_INVALID_SYNTAX, "Email field contains string of invalid syntax.")

ACCOUNT_ALREADY_EXISTS = 105
ez_update(ACCOUNT_ALREADY_EXISTS, "An account with the same email already exists.")

PHONE_NUMBER_INVALID = 106
ez_update(PHONE_NUMBER_INVALID, "Phone number field contains string of invalid syntax.")

FULL_NAME_INVALID_LENGTH = 107
ez_update(FULL_NAME_INVALID_LENGTH, "Full name field contains string of invalid length.")

EMAIL_PASSWORD_INVALID = 108
ez_update(EMAIL_PASSWORD_INVALID, "Email or Password is incorrect.")


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
#########################

# charger [200-299]
CHARGER_WITH_FAVOURITE = 200
ez_update(CHARGER_WITH_FAVOURITE, "Charger list with favourites.")

CHARGER_WITHOUT_FAVOURITE = 201
ez_update(CHARGER_WITHOUT_FAVOURITE, "Charger list without favourites.")


CHARGER_FOUND = 299
ez_update(CHARGER_FOUND, "Chargers found.")

CHARGER_NOT_FOUND = 298
ez_update(CHARGER_NOT_FOUND, "Chargers not found.")
#########################

# charger_available_connector [300-399]
AVAILABLE_CONNECTORS_NOT_FOUND = 399
ez_update(AVAILABLE_CONNECTORS_NOT_FOUND, "Charger connector types found.")

AVAILABLE_CONNECTORS_FOUND = 398
ez_update(AVAILABLE_CONNECTORS_FOUND, "Charger connector types not found.")
#########################

# connector_type [400-499]
CONNECTOR_FOUND = 499
ez_update(CONNECTOR_FOUND, "Connector type definitions found.")

CONNECTOR_NOT_FOUND = 498
ez_update(CONNECTOR_NOT_FOUND, "Connector type definitions not found.")
#########################

# favourited_chargers [500-599]
FAVOURITE_CHARGER_MODIFY_ILLEGAL_OPERATION = 500
ez_update(FAVOURITE_CHARGER_MODIFY_ILLEGAL_OPERATION, "Illegal favourite modify favourite operation specified.")

FAVOURITE_CHARGER_MODIFY_INVALID_OPERATION = 501
ez_update(FAVOURITE_CHARGER_MODIFY_INVALID_OPERATION, "Invalid favourite modify favourite operation specified.")

FAVOURITE_CHARGER_DUPLICATE_ENTRY = 502
ez_update(FAVOURITE_CHARGER_DUPLICATE_ENTRY, "A similar favourite charger already exists.")

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
VEHICLE_NAME_INVALID_LENGTH = 600
ez_update(VEHICLE_NAME_INVALID_LENGTH, "Vehicle name field contains string of invalid length.")

VEHICLE_MODEL_INVALID_LENGTH = 601
ez_update(VEHICLE_MODEL_INVALID_LENGTH, "Vehicle model field contains string of invalid length.")

VEHICLE_SN_INVALID_LENGTH = 602
ez_update(VEHICLE_SN_INVALID_LENGTH, "Vehicle SN field contains string of invalid length.")


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
CHARGE_HISTORY_INVALID_CHARGE_LEVEL = 700
ez_update(CHARGE_HISTORY_INVALID_CHARGE_LEVEL, "Invalid battery percentage specified.")

CHARGE_HISTORY_ALREADY_CHARGING = 701
ez_update(CHARGE_HISTORY_ALREADY_CHARGING, "Can't start a new charge while already charging.")

CHARGE_HISTORY_NOT_CHARGING = 702
ez_update(CHARGE_HISTORY_NOT_CHARGING, "Can't finish a charge, this user does not have an unfinished entry.")

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
CURRENCY_INVALID = 800
ez_update(CURRENCY_INVALID, "Currency field contains string of invalid syntax.")

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
#########################