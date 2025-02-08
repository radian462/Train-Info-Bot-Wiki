import os
import time
from datetime import datetime
from threading import Thread

from dotenv import load_dotenv

from Modules.Clients.bluesky import Bluesky
from Modules.healthcheck import healthcheck
from Modules.make_logger import make_logger
from Modules.traininfo import TrainInfo

healthcheck()
load_dotenv()
logger = make_logger("main")


class RegionalManager:
    def __init__(self, region):
        self.account_datas = {
            "関東": {
                "Bluesky": {
                    "name": os.getenv(f"BLUESKY_KANTO_NAME"),
                    "password": os.getenv(f"BLUESKY_KANTO_PASS"),
                }
            },
            "関西": {
                "Bluesky": {
                    "name": os.getenv(f"BLUESKY_KANSAI_NAME"),
                    "password": os.getenv(f"BLUESKY_KANSAI_PASS"),
                }
            },
        }

        self.region = region
        self.train_info = TrainInfo(region)
        self.bluesky = Bluesky(
            self.account_datas[self.region]["Bluesky"]["name"],
            self.account_datas[self.region]["Bluesky"]["password"],
            region,
        )

    def execute(self):
        data = self.train_info.request()
        messages = self.train_info.make_message(data)
        self.bluesky.post(messages)


def main():
    regions = ["関東", "関西"]
    managers = [RegionalManager(region) for region in regions]

    interval = 10
    while True:
        minutes, seconds = datetime.now().minute, datetime.now().second

        threads = []
        if minutes % interval == 0:
            threads = [Thread(target=manager.execute) for manager in managers]
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            threads = []

        next_minute = (minutes // interval + 1) * interval
        wait_time = (next_minute - minutes) * 60 - seconds
        logger.info(f"Sleep {wait_time} seconds")
        time.sleep(wait_time)


if __name__ == "__main__":
    main()
