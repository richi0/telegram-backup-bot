from pathlib import Path

from settings import file_location


class FileHandler:
    def __init__(self):
        self.handler = self.get_handler()

    def get_handler(self):
        if file_location == "google":
            return GoogleDriveHandler()
        else:
            return LocalHandler()


class LocalHandler:
    def save(self, file_name, file):
        with open(Path("data", file_name), "wb") as fp:
            file.seek(0)
            fp.write(file.read())
            return True

    def read(self, file_name):
        return open(Path("data", file_name), "rb")

class GoogleDriveHandler:
    def save(self, file_name, file):
        with open(Path("data", file_name), "wb") as fp:
            file.seek(0)
            fp.write(file)
            return True

    def read(self, file_name):
        with open(Path("data", file_name), "rb") as fp:
            return fp.read()