from flask import Blueprint

auth_v1 = Blueprint('auth', __name__, url_prefix='/v1/auth')
from .views import *
