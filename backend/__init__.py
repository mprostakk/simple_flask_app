from flask import Flask
from backend.extension import db, jwt, bcrypt
import os
import datetime


def create_app():
    app = Flask(__name__.split('.')[0])

    db_env = os.getenv('MONGO_DB', '')

    app.config['MONGODB_SETTINGS'] = {
        'db': 'taskproject1',
        'host': db_env,
        'port': 27017
    }

    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

    register_extensions(app)
    register_blueprints(app)

    app.app_context().push()

    from backend.models.task import Task

    return app


def register_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)


def register_blueprints(app):
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp, url_prefix='/api')
