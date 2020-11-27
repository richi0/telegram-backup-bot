from datetime import date
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String)
    name = Column(String)
    authorized = Column(Boolean, default=False)
    created = Column(String, default=date.today().strftime("%Y-%m-%d"))

    def __repr__(self):
        return f"<User name={self.name} id={self.id}>"
