from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import db_logging
from models import User, Base


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
