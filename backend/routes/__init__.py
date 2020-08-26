from flask import Blueprint

bp = Blueprint('routes', __name__)

from backend.routes.task import *
from backend.routes.auth import *
