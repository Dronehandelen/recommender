from google.cloud import storage
import logging

from app.exceptions.fileNotFound import FileNotFound
from app.storage.storage import Storage


class GoogleCloudStorage(Storage):
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_name = "dh-recommender"

    def download_blob(self, source_blob_name, destination_file_name):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        blob = bucket.blob(source_blob_name)

        if not blob.exists():
            raise FileNotFound

        blob.download_to_filename(destination_file_name)

        logging.info('Blob {} downloaded to {}.'.format(
            source_blob_name,
            destination_file_name
        ))

    def list_folder_files(self, bucket, folder):
        return self.storage_client.list_blobs(bucket_or_name=bucket, prefix=folder + "/")

    def get_last_recommender_path(self, folder_name):
        files = self.list_folder_files(self.bucket_name, folder_name)

        recommender_path = None
        recommender_timestamp = None

        for file in files:
            if file.name.endswith("/"):
                continue

            file_parts = file.name.split("/")

            if len(file_parts) != 2:
                continue

            file_name = file_parts[1]

            suffix = ".csv"
            if not file_name.endswith(suffix):
                continue

            file_name_timestamp = int(file_name[:-len(suffix)])

            if recommender_path is None or file_name_timestamp > recommender_timestamp:
                recommender_path = file.name
                recommender_timestamp = file_name_timestamp

        return recommender_path, recommender_timestamp
