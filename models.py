from datetime import date
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String)
    name = Column(String)
    authorized = Column(Boolean, default=False)
    created = Column(String, default=date.today().strftime("%Y-%m-%d"))
    files = relationship("File", order_by="File.id", back_populates="creator")

    def __repr__(self):
        return f"<User name={self.name} id={self.id}>"


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    file_name = Column(String)
    unique_name = Column(String)
    saved = Column(String, default=date.today().strftime("%Y-%m-%d"))
    extension = Column(String)
    file_type = Column(String)
    size = Column(Integer)

    creator = relationship("User", back_populates="files")
