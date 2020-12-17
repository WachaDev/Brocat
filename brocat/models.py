from flask_login import UserMixin, current_user
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from bcrypt import hashpw, checkpw, gensalt
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from brocat.database import Base


class Users(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    e_mail = Column('e-mail', String(30), nullable=False, unique=True)
    username = Column(String(16), nullable=False, unique=True)
    __password = Column('password', String(16), nullable=False)

    brocats = relationship('Brocats', back_populates='author')

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


class Brocats(Base):
    __tablename__ = 'brocats'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=True)
    thumbnail = Column(String(200), nullable=False)
    audio = Column(String(200), nullable=False)
    description = Column(String(500))

    users_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('Users', back_populates='brocats')

    def __init__(self, title, thumbnail, audio, description):
        self.title = title
        self.thumbnail = thumbnail
        self.audio = audio
        self.description = description
        self.author = current_user


# * SCHEMAS

class UsersSchema(SQLAlchemySchema):
    class Meta:
        model = Users

    id = auto_field()
    e_mail = auto_field()
    username = auto_field()
    brocats = auto_field()


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)


class BrocatsSchema(SQLAlchemySchema):
    class Meta:
        model = Brocats

    title = auto_field()
    thumbnail = auto_field()
    audio = auto_field()
    description = auto_field()
    users_id = auto_field()
    author = auto_field()


brocat_schema = BrocatsSchema()
brocats_schema = BrocatsSchema(many=True)
