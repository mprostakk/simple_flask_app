from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt


db = MongoEngine()
jwt = JWTManager()
bcrypt = Bcrypt()
