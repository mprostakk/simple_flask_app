from flask import Flask
from backend.extension import db, jwt, bcrypt, scheduler
import os
import datetime
import atexit


def create_app():
    app = Flask(__name__.split('.')[0])

    db_env = os.getenv('MONGO_DB', '')
    db_port = int(os.getenv('MONGO_PORT', 27017))
    db_name = os.getenv('MONGO_NAME', 'test-project1')

    app.config['MONGODB_SETTINGS'] = {
        'db': db_name,
        'host': db_env,
        'port': db_port
    }

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_KEY', 'test-secret')
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

    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


def register_blueprints(app):
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp, url_prefix='/api')
