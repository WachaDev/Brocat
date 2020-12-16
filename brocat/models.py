from flask_login import UserMixin, current_user
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from bcrypt import hashpw, checkpw, gensalt

from brocat.database import Base


class UserSchema(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    e_mail = Column('e-mail', String(30), nullable=False, unique=True)
    username = Column(String(16), nullable=False, unique=True)
    __password = Column('password', String(16), nullable=False)

    brocats = relationship('BrocatSchema', back_populates='author')

    def __init__(self, email, username, password):
        self.e_mail = email
        self.username = username
        self.password = password

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        hashed_psw = hashpw(value.encode('UTF-8'), gensalt())
        self.__password = hashed_psw

    def check_psw(self, psw):
        return checkpw(psw.encode('UTF-8'), self.__password)

    def __repr__(self):
        return self.username


class BrocatSchema(Base):
    __tablename__ = 'brocats'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=True)
    thumbnail = Column(String(200), nullable=False)
    audio = Column(String(200), nullable=False)
    description = Column(String(500))

    users_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('UserSchema', back_populates='brocats')

    def __init__(self, title, thumbnail, audio, description):
        self.title = title
        self.thumbnail = thumbnail
        self.audio = audio
        self.description = description
        self.author = current_user
    
