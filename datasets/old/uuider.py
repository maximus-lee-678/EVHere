import datetime
import uuid
import csv

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

with open("./datasets/chargers_base.csv", 'r', encoding='UTF-8') as file:
    rows = [line.rstrip() for line in file]

for count, row in enumerate(rows):
    if count == 0:
        charger_rows.append("id" + "," + row + "," + "last_updated" + "\n")
    else:
        charger_rows.append(str(uuid.uuid4()) + "," +
                            row + "," + time_now + "\n")

with open("./datasets/chargers_modded.csv", 'w', encoding='UTF-8') as file:
    rows = [file.write(line) for line in charger_rows]

#####

with open("./datasets/connectors_base.csv", 'r', encoding='UTF-8') as file:
    rows = [line.rstrip() for line in file]

for count, row in enumerate(rows):
    if count == 0:
        connector_rows.append("id" + "," + row + "\n")
    else:
        new_uuid = str(uuid.uuid4())
        charger_connector_uuid_map.append(
            {"name": row.split(',')[0], "id": new_uuid})
        connector_rows.append(new_uuid + "," + row + "\n")

with open("./datasets/connectors_modded.csv", 'w', encoding='UTF-8') as file:
    rows = [file.write(line) for line in connector_rows]

#####
reader = csv.reader(charger_rows)
for row in reader:
    charger_rows_2d.append(row)

for count, row in enumerate(charger_rows_2d):
    if count == 0:
        charger_connectors_rows.append("id,id_charger,id_connector_type\n")
    else: # i lazy update to 3.10
        if row[5] == "Bluecharge":  # DC
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "DC")['id'] + "\n")
        elif row[5] == "SPMobility":    # Dual & DC
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "Dual")['id'] + "\n")
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "DC")['id'] + "\n")
        elif row[5] == "Plugshare":    # AC
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "AC")['id'] + "\n")
        elif row[5] == "Shell":    # Dual
            charger_connectors_rows.append(str(uuid.uuid4()) + "," + row[0] + "," + next(
                item for item in charger_connector_uuid_map if item["name"] == "Dual")['id'] + "\n")
            
with open("./datasets/chargers_connectors_modded.csv", 'w', encoding='UTF-8') as file:
    rows = [file.write(line) for line in charger_connectors_rows]
