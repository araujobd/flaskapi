from flask_marshmallow.sqla import SchemaOpts
from marshmallow import post_dump, validates, ValidationError
from marshmallow import fields
from sqlalchemy.exc import SQLAlchemyError

from api.common.database import ma, db


class BaseOpts(SchemaOpts):
    def __init__(self, meta):
        if not hasattr(meta, "sqla_session"):
            meta.sqla_session = db.session
        super(BaseOpts, self).__init__(meta)
        self.singular = getattr(meta, 'singular', None)
        self.plural = getattr(meta, 'plural', None)


class BaseSchema(ma.ModelSchema):
    OPTIONS_CLASS = BaseOpts

    id = fields.Str(required=True)
    active = fields.Boolean()

    def get_envelope_key(self, many):
        key = self.opts.plural if many else self.opts.singular
        if key is None:
            key = 'data'
        return key

    @validates('id')
    def validate_uuid(self, id):
        if not id.isalnum() or not len(id) == 32:
            raise ValidationError('Is not a UUID valid')

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many):
        key = self.get_envelope_key(many)
        return {key: data}

    @classmethod
    def get_collection(cls):
        entity = cls.Meta.model
        data = entity.query.all()
        collection = cls(many=True).dump(data)
        return collection.data

    @classmethod
    def create_object(cls, payload):
        code = 422
        data, errors = cls().load(payload)
        if not errors:
            db.session.add(data)
            try:
                db.session.commit()
                data = cls().dump(data).data
                code = 201
            except SQLAlchemyError as e:
                db.session.rollback()
                error = []
                for err in e.args:
                    error.append(str(err))
                errors = {"errors": error}
                code = 400
        return data, errors, code
