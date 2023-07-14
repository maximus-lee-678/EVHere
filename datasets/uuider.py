import datetime
import uuid
import csv
import random

CHARGER_PATH_IN = "./datasets/chargers_base_v2.csv"
CHARGER_PATH_OUT = "./datasets/chargers_modded.csv"
CONNECTOR_PATH_IN = "./datasets/connectors_base.csv"
CONNECTOR_PATH_OUT = "./datasets/connectors_modded.csv"
CHARGER_CONNECTOR_OUT = "./datasets/chargers_connectors_modded.csv"

rows = []

# for chargers
charger_rows = []

# for connectors
connector_rows = []

# for charger connectors
charger_connectors_rows = []
charger_rows_2d = []
charger_connector_uuid_map = []

time_now = str(datetime.datetime.now())

with open(CHARGER_PATH_IN, 'r', encoding='UTF-8') as file:
    rows = [line.rstrip() for line in file]

for count, row in enumerate(rows):
    if count == 0:
        charger_rows.append("id" + "," + row + "," + "last_updated" + "\n")
    else:
        charger_rows.append(str(uuid.uuid4()) + "," +
                            row + "," + time_now + "\n")

with open(CHARGER_PATH_OUT, 'w', encoding='UTF-8') as file:
    rows = [file.write(line) for line in charger_rows]

#####

with open(CONNECTOR_PATH_IN, 'r', encoding='UTF-8') as file:
    rows = [line.rstrip() for line in file]

for count, row in enumerate(rows):
    if count == 0:
        connector_rows.append("id" + "," + row + "\n")
    else:
        new_uuid = str(uuid.uuid4())
        charger_connector_uuid_map.append(
            {"name": row.split(',')[0], "id": new_uuid})
        connector_rows.append(new_uuid + "," + row + "\n")

with open(CONNECTOR_PATH_OUT, 'w', encoding='UTF-8') as file:
    rows = [file.write(line) for line in connector_rows]

#####
reader = csv.reader(charger_rows)
for row in reader:
    charger_rows_2d.append(row)

for count, row in enumerate(charger_rows_2d):
    if count == 0:
        charger_connectors_rows.append("id,id_charger,id_connector_type,in_use,output_current\n")
    else: 
        # disgusting
        dice = random.random()

        if dice < 0.14:     # 001
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "DC")['id'] + ",false,0\n")
        elif dice < 0.28:    # 010
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "Dual")['id'] + ",false,0\n")
        elif dice < 0.42:   # 011
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "DC")['id'] + ",false,0\n")
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "Dual")['id'] + ",false,0\n")
        elif dice < 0.56:      # 100
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "AC")['id'] + ",false,0\n")
        elif dice < 0.7:    # 101
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "AC")['id'] + ",false,0\n")
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "DC")['id'] + ",false,0\n")
        elif dice < 0.84:   # 110
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "AC")['id'] + ",false,0\n")
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "Dual")['id'] + ",false,0\n")
        else:   # 111
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "AC")['id'] + ",false,0\n")
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "Dual")['id'] + ",false,0\n")
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "DC")['id'] + ",false,0\n")

with open(CHARGER_CONNECTOR_OUT, 'w', encoding='UTF-8') as file:
    rows = [file.write(line) for line in charger_connectors_rows]
