"""This module contains objects to save Files on various locations."""
import io
from pathlib import Path

import dropbox

from settings import storage_location, dropbox_api_token


class StorageHandler:
    """An object to save files depending on storage settings.
    This makes it possible to implement various storage backend
    easily. Backends must provide a save, read and delete methode.
    """

    def __init__(self):
        self.storage = self.get_handler()

    def get_handler(self):
        """Returns the storage handler depending on the storage_location settings"""
        if storage_location == "dropbox":
            return DropboxStorage()
        else:
            return LocalStorage()


class LocalStorage:
    """Provides methodes to save, read and delete files from the local file system.
    This is the default StorageHandler.
    """

    def save(self, file_name, file):
        """Returns true if the file was saved successfully"""
        with open(Path("data", file_name), "wb") as fp:
            file.seek(0)
            fp.write(file.read())
            return True

    def read(self, file_name):
        """Returns the file with the matching file_name

        Args:
            - file_name (str): The file name is the complete name including the suffix
                               example: test_file.txt
        """
        return open(Path("data", file_name), "rb")


class DropboxStorage:
    """Provides methodes to save, read and delete files from dropbox. This can
    be useful if you deploy your bot to a free service where you cannot save
    static files directly. To use it set your storage_location to 'dropbox'.
    To use this storage backend you need to get a dropbox_api_token.

    Follow the dropbox guide to get a token:
        - https://www.dropbox.com/developers/documentation/python#tutorial
    """

    def __init__(self):
        self.dbx = dropbox.Dropbox(dropbox_api_token)

    def save(self, file_name, file):
        """Returns true if the upload to dropbox was successful."""
        file.seek(0)
        self.dbx.files_upload(file.read(), "/" + file_name)
        return True

    def read(self, file_name):
        """Returns the file after downloading it from dropbox."""
        meta_data, response = self.dbx.files_download("/" + file_name)
        return io.BytesIO(response.content)
