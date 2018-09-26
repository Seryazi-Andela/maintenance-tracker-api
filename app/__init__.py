from flask import Flask

app = Flask(__name__)

from .authentication import auth_v1

app.register_blueprint(auth_v1)
