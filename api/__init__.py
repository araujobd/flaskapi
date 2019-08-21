from flask import Blueprint
from flask_restplus import Api
from importlib import import_module

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, version='1.0.0', description='A api')


def transform_module_name(module):
    return 'api.' + module + '.resource'


def init_modules(modules):
    for module in modules:
        namespace = import_module(transform_module_name(module))
        api.add_namespace(namespace.api)
