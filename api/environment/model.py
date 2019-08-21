from flask_restplus import fields, Model

from api.common.database import db
from api.common.entity import Entity
from api.common.schemas import BaseSchema


class Environment(Entity, db.Model):
    name = db.Column(db.String(80), nullable=False)
    local = db.Column(db.String(80), nullable=False)


class EnvironmentSchema(BaseSchema):
    class Meta:
        model = Environment
        singular = 'environment'
        plural = 'environments'


environmentModel = Model('Environment', {
    'id': fields.String,
    'active': fields.Boolean,
    'name': fields.String,
    'local': fields.String
})
