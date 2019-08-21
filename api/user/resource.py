from flask_restplus import Namespace

from api.common.resource import EntityCollectionResource, EntityResource
from api.user.model import UserSchema, userModel

api = Namespace('users', description='Açoes relacionadas a usuários')
api.models[userModel.name] = userModel


@api.route('')
class UsersResource(EntityCollectionResource):
    schema = UserSchema

    @api.expect(userModel)
    def post(self):
        return super().post()


@api.route('/<string:id>')
@api.param('id', 'User identifier')
class UserResource(EntityResource):
    schema = UserSchema
