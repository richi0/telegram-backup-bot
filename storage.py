from pathlib import Path

import dropbox

from settings import storage_location, dropbox_api_token


class StorageHandler:
    def __init__(self):
        self.storage = self.get_handler()

    def get_handler(self):
        if storage_location == "dropbox":
            return DropboxStorage()
        else:
            return LocalStorage()


class LocalStorage:
    def save(self, file_name, file):
        with open(Path("data", file_name), "wb") as fp:
            file.seek(0)
            fp.write(file.read())
            return True

    def read(self, file_name):
        return open(Path("data", file_name), "rb")

class DropboxStorage:
    def __init__(self):
        self.dbx = dropbox.Dropbox(dropbox_api_token)

    def save(self, file_name, file):
        return None

    def read(self, file_name):
        return None

if __name__ == "__main__":
    handler = DropboxStorage()
