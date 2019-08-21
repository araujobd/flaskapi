from api.common.database import db


class Entity(object):
    id = db.Column(db.String(32), primary_key=True)
    active = db.Column(db.Boolean())


def get_collection(schema_cls, cls):
    schema = schema_cls(many=True)
    data = cls.query.all()

    return schema.dump(data)
