from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from .authentication import auth_v1
from .application import apcn_v1
from .administrator import admin_v1

app.register_blueprint(auth_v1)
app.register_blueprint(apcn_v1)
app.register_blueprint(admin_v1)
