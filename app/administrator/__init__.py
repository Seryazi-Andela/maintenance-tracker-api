from flask import Blueprint

admin_v1 = Blueprint('admin', __name__,  url_prefix='/v1')
from .views import *
