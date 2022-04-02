import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
import datetime
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, name='surname')
    name = sqlalchemy.Column(sqlalchemy.String, name='name')
    age = sqlalchemy.Column(sqlalchemy.Integer, name='age')
    town = sqlalchemy.Column(sqlalchemy.String, name='town', default='Moscow')
    email = sqlalchemy.Column(sqlalchemy.String, name='email')
    password = sqlalchemy.Column(sqlalchemy.String, name='password')
    register_date = sqlalchemy.Column(sqlalchemy.DateTime, name='register_date', default=datetime.datetime.now())
    products = orm.relation("Products", back_populates='user')