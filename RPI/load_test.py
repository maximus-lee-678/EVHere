from locust import HttpUser, task, between
from time import sleep
import datetime
import requests
import json


class MyUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def server_post(self):
        cnt = 0
        # random ids from the database, fill this with string of charger uuids
        ev_id = [

        ]

        if not ev_id:
            print("initialise ev_id array!")
            exit()

        # test not gated by database capabilities
        while True:
            self.client.get("api/handshake")
            sleep(1)

        # test with simulated post method; will be gated by database capabilities
        # while True:
        #     data = {
        #         "id": ev_id[cnt],
        #         "pv_voltage_in": 4.38,
        #         "pv_current_in": 0.44,
        #         "pv_voltage_out": 2.11,
        #         "pv_current_out": 0.21,
        #         "pv_timestamp": datetime.datetime.now().isoformat(
        #             sep="T", timespec="auto"
        #         ),
        #     }
        #     headers = {"Content-Type": "application/json"}

        #     self.client.post(
        #         "api/update_charger", data=json.dumps(data), headers=headers
        #     )
        #     cnt += 1
        #     sleep(1)
