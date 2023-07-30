# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep
import datetime
import sqlite3
import requests
import json

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)

cnt=0
total_chan=0
total_chan1=0

# count for periodic measurement and transmission
# set to 1 for 1 s, 60 for 1 min, 900 for 15 min, 3600 for 1 hr
duration=1

# test id to confirm change of value
first_id = "00cca3e8-75fe-47d0-8f6a-468493f47c53"

# ip address and api endpoints for connection
hsip4 = 'http://192.168.145.84:5000/api/update_charger'
hsip4g = 'http://192.168.145.84:5000/api/get_all_chargers'
hsip5 = 'http://192.168.143.84:5000/api/update_charger'
hsip5g = 'http://192.168.143.84:5000/api/get_all_chargers'
con = hsip4

try:
    while True:
        # recording the time stamp
        timestamp = datetime.datetime.now()
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")        
        
        # doubling the voltage halved by the voltage divider circuit
        adjusted_chan = (chan.voltage) * 2
        total_chan += adjusted_chan
        adjusted_chan1 = (chan1.voltage) * 2
        total_chan1 += adjusted_chan1
        
        sleep(1)
        
        # calculate average at regular interval
        cnt+=1
        if(cnt==duration):
            cnt=0
            average_chan = total_chan / duration
            average_chan1 = total_chan1 / duration
            total_chan = 0
            total_chan1 = 0
            
            voltage_in = "{:.2f}".format(adjusted_chan)
            current_in = "{:.2f}".format(adjusted_chan / 10000 * 1000)
            voltage_out = "{:.2f}".format(adjusted_chan1)
            current_out = "{:.2f}".format(adjusted_chan1 / 10000 * 1000)

            headers = {'Content-Type':"application/json"}

            # get data from server
            get_response = requests.get(con, headers=headers)
            api_response = get_response.json()
            get_data = api_response.get("data", [])
            print("in")
            if get_data and isinstance(get_data,list) and len(get_data) > 0:
                first_id=get_data[0].get('id')
                print(first_id)
                
            # post data to server
            post_data = {'id': first_id,
                        'pv_voltage_in': voltage_in,
                        'pv_current_in': current_in,
                        'pv_voltage_out': voltage_out,
                        'pv_current_out': current_out,
                        'pv_timestamp': datetime.datetime.now().isoformat(sep='T',timespec='auto')}
            
            print(post_data)
            response = requests.post(con, data=json.dumps(post_data), headers=headers)
            print(response.text)
        
except KeyboardInterrupt:
    print('end')