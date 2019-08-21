from flask_restplus import Namespace

from api.common.resource import EntityCollectionResource, EntityResource
from api.environment.model import environmentModel, EnvironmentSchema

api = Namespace('environments', description='Ações relacionadas a ambientes')
api.models[environmentModel.name] = environmentModel


@api.route('')
class EnvironmentsResource(EntityCollectionResource):
    schema = EnvironmentSchema

    @api.expect(environmentModel)
    def post(self):
        return super().post()


@api.route('/<string:id>')
@api.param('id', 'Environment identifier')
class EnvironmentResource(EntityResource):
    schema = EnvironmentSchema
