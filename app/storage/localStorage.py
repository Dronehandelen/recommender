import logging

from app.exceptions.fileNotFound import FileNotFound
from app.storage.storage import Storage
from shutil import copyfile
import os.path
from os import listdir
from os.path import isfile, join


def list_folder_files(folder):
    return [f for f in listdir(folder) if isfile(join(folder, f))]


class LocalStorage(Storage):
    base_folder = "./bucketish"

    def download_blob(self, source_blob_name, destination_file_name):
        if not os.path.isfile(source_blob_name):
            raise FileNotFound

        os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)
        copyfile(source_blob_name, destination_file_name)

        logging.info('Blob {} downloaded to {}.'.format(
            source_blob_name,
            destination_file_name
        ))

    def get_last_recommender_path(self, folder_name):
        files = list_folder_files(join(self.base_folder, folder_name))
        recommender_path = None
        recommender_timestamp = None

        for file in files:
            suffix = ".csv"
            if not file.endswith(suffix):
                continue

            file_name_timestamp = int(file[:-len(suffix)])
            if recommender_path is None or file_name_timestamp > recommender_timestamp:
                recommender_path = file
                recommender_timestamp = file_name_timestamp

        return join(self.base_folder, folder_name, recommender_path), recommender_timestamp
