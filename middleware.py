"""This module contains an object that represents a Request to the bot."""
import uuid

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import db_logging
from models import Base, User, File
from storage import StorageHandler


class Request:
    """Every message to the bot will be connected to a Request object.
    This helps to check if a user is authenticated and provieds methodes
    to return, save and delete files.
    """

    def __init__(self, update):
        self.update = update
        self.telegram_id = self.update.message.chat.id
        self.engine = create_engine('sqlite:///data.db', echo=db_logging)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.user = self.get_user()
        self.storage_handler = StorageHandler()

    def get_user(self):
        """Returns an existing user or creates a new one if the user doesn't exist."""
        user = self.session.query(User).filter_by(
            telegram_id=self.telegram_id).first()
        if user:
            return user
        else:
            return self.create_user()

    def create_user(self):
        """Returns a new user"""
        user = User(name=self.update.message.chat.first_name,
                    telegram_id=self.telegram_id)
        self.session.add(user)
        self.session.commit()
        return user

    def authorize_user(self):
        """Sets a user authorization to true."""
        self.user.authorized = True
        self.session.commit()

    def add_file(self, info, doc):
        """Saves the meta data of a file in the database and the file
        depending of the storage handler on the file system or in the cloud.
        """
        file = File(
            creator_id=self.user.id,
            file_name=info["file_name"],
            unique_name=str(uuid.uuid4())+info["extension"],
            extension=info["extension"],
            file_type=info["file_type"],
            size=int(info["size"])
        )
        self.session.add(file)
        self.session.commit()

        self.storage_handler.storage.save(file.unique_name, doc)

    def get_all_files(self):
        """Returns meta data of all saved files"""
        files = self.session.query(File).all()
        return files

    def return_file(self, id):
        """returns a single file matched with id"""
        file_data = self.session.query(File).filter_by(id=id).first()
        return file_data
