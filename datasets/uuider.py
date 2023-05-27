import datetime
import uuid

rows = []
guid_rows = []
time_now = str(datetime.datetime.now())

with open("./datasets/og.csv", 'r', encoding='UTF-8') as file:
    rows = [line.rstrip() for line in file]

for count, row in enumerate(rows):
    if count == 0:
        guid_rows.append("id" + "," + row + "," + "last_updated" + "\n")
    else:
        guid_rows.append(str(uuid.uuid4()) + "," + row + "," + time_now + "\n")

with open("./datasets/guid_timed.csv", 'w', encoding='UTF-8') as file:
    rows = [file.write(line) for line in guid_rows]
