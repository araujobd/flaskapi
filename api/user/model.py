from flask_restplus import Model, fields

from api.common.database import db
from api.common.entity import Entity
from api.common.schemas import BaseSchema


class User(Entity, db.Model):
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    login = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=True)


class UserSchema(BaseSchema):
    class Meta:
        model = User
        singular = 'user'
        plural = 'users'
        fields = ("id", "active", "name", "email", "login")


userModel = Model('User', {
    'id': fields.String,
    'name': fields.String,
    'email': fields.String,
    'login': fields.String,
    'password': fields.String,
    'active': fields.Boolean
})
