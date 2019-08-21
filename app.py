from flask import Flask

from api.common.database import init_database
from api import api_blueprint, init_modules


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    modules = ['user', 'environment']
    with app.app_context():
        init_modules(modules)
        init_database(app)
        app.register_blueprint(api_blueprint)
    return app


if __name__ == '__main__':
    my_app = create_app()
    my_app.run(host='0.0.0.0', debug=True)
