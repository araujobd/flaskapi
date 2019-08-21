from flask import request
from flask_restplus import Resource
from sqlalchemy.exc import SQLAlchemyError

from api.common.database import db


class EntityCollectionResource(Resource):
    schema = None

    def get(self):
        return self.get_collection(), 200

    def post(self):
        payload = request.get_json() or None

        data, errors, code = self.create_object(payload)
        if errors:
            return errors, code
        return data, code

    def get_collection(self):
        entity = self.schema.Meta.model
        entities = entity.query.all()
        collection = self.schema(many=True).dump(entities)
        return collection.data

    def create_object(self, payload):
        schema = self.schema()
        code = 422
        data, errors = schema.load(payload)
        if not errors:
            db.session.add(data)
            try:
                db.session.commit()
                data = schema.dump(data).data
                code = 201
            except SQLAlchemyError as e:
                db.session.rollback()
                error = []
                for err in e.args:
                    error.append(str(err))
                errors = {"errors": error}
                code = 400
        return data, errors, code


class EntityResource(Resource):
    schema = None

    def get_entity(self, entity_id):
        entity_cls = self.schema.Meta.model
        return entity_cls.query.get(entity_id)

    def get(self, id):
        entity = self.get_entity(id)
        if not entity:
            error = {"error": "entity not found"}
            return error, 404
        return self.schema().dump(entity).data, 200

    def put(self):
        pass

    def delete(self, id):
        entity = self.get_entity(id)
        if not entity:
            error = {"error": "entity not found"}
            return error, 404
        try:
            db.session.delete(entity)
            db.session.commit()
            return self.schema().dump(entity), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            error = {"error": str(e.args)}
            return error, 404
