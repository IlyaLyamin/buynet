import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Products(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    product = sqlalchemy.Column(sqlalchemy.String, default='без названия')
    price = sqlalchemy.Column(sqlalchemy.Integer)
    photo = sqlalchemy.Column(sqlalchemy.BLOB, default=None)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    about = sqlalchemy.Column(sqlalchemy.String, default='Без описания')

    user = orm.relation('User')