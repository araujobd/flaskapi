from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def init_database(app):
    db.init_app(app)
    db.create_all()
    ma.init_app(app)
