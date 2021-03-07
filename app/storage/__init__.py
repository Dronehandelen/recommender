from app.config.app import is_prod
from app.storage.googleCloudStorage import GoogleCloudStorage
from app.storage.localStorage import LocalStorage
from app.storage.storage import Storage


def get_storage() -> Storage:
    if is_prod is True:
        return GoogleCloudStorage()
    else:
        return LocalStorage()
