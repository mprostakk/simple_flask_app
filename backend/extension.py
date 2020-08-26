from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from apscheduler.schedulers.background import BackgroundScheduler


db = MongoEngine()
jwt = JWTManager()
bcrypt = Bcrypt()
scheduler = BackgroundScheduler()