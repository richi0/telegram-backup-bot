import uuid

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import db_logging
from models import Base, User, File


class Request:
    def __init__(self, update):
        self.update = update
        self.telegram_id = self.update.message.chat.id
        self.engine = create_engine('sqlite:///data.db', echo=db_logging)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.user = self.get_user()

    def get_user(self):
        user = self.session.query(User).filter_by(
            telegram_id=self.telegram_id).first()
        if user:
            return user
        else:
            return self.create_user()

    def create_user(self):
        user = User(name=self.update.message.chat.first_name,
                    telegram_id=self.telegram_id)
        self.session.add(user)
        self.session.commit()
        return user

    def authorize_user(self):
        self.user.authorized = True
        self.session.commit()

    def add_file(self, info, doc):
        file = File(
            creator_id=self.user.id,
            file_name=info["file_name"],
            unique_name=str(uuid.uuid4())+info["extension"],
            extension=info["extension"],
            size=int(info["size"])
        )
        self.session.add(file)
        self.session.commit()

        print(file.extension)
        print(file.unique_name)
        print(file.file_name)

        with open(Path("data", file.unique_name), "wb") as fp:
            doc.seek(0)
            fp.write(doc.read())
