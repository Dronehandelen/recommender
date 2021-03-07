import logging
import os
import time
import pandas as pd
from app.storage import get_storage

storage = get_storage()

class Rater:
    last_check = None
    corr_table = None
    recommender_path = None

    def __init__(self, name, folder_name):
        self.update_check_interval = 300  # Seconds -> 5min
        self.name = name
        self.folder_name = folder_name
        self.update_recommender()

    def update_recommender(self):
        logging.info(f"Checking for corr_table updates")

        self.last_check = time.time()

        new_path, recommender_timestamp = storage.get_last_recommender_path(self.folder_name)

        if new_path == self.recommender_path:
            logging.info(f"No new corr_table found. Returning current {recommender_timestamp}")
            return

        self.recommender_path = new_path
        csv_file = "./tmp/{}/{}.csv".format(self.folder_name, recommender_timestamp)

        os.makedirs(os.path.dirname(csv_file), exist_ok=True)

        if not os.path.isfile(csv_file):
            storage.download_blob(new_path, csv_file)
        else:
            logging.info(f"Corr table is already available locally {csv_file}")

        raw_data = pd.read_csv(csv_file)
        self.corr_table = self.get_corr_table(raw_data)

    def get_corr_table(self, csv_data):
        pass

    def rate(self, product_ids):
        if self.corr_table is None:
            logging.error("Rater {} has no corr_table".format(self.folder_name))
            return None

        merged_rates = None

        for productId in product_ids:
            if productId not in self.corr_table.index:
                continue

            if merged_rates is None:
                merged_rates = self.corr_table[productId]
            else:
                merged_rates = merged_rates + self.corr_table[productId]

        if merged_rates is None:
            return None

        df = pd.DataFrame(data=merged_rates)

        df.columns = [self.name]
        return df
