from flask_restful import Resource, Api, reqparse
from flask import jsonify, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_raw_jwt, get_jwt_identity)

from .models import User
from . import auth_v1
from ..app_utils.utils import empty_string_catcher, isString, isInteger, email_validator, isBool
from ..database.db_handler import DBHandler


api = Api(auth_v1)


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        username = data['username']
        password = generate_password_hash(data['password'], method='sha256')
        admin = data['admin']

        if not empty_string_catcher(email) or not empty_string_catcher(username) or not empty_string_catcher(password):
            return make_response(jsonify({'message': 'please fill all fields'}), 400)

        if not isString(email) or not isString(username) or not isString(password) or not isBool(admin):
            return make_response(jsonify({'message': 'please insert correct values'}), 400)

        if not email_validator(email):
            return make_response(jsonify({'message': 'malformed email'}), 400)

        user = User(email, username, password, admin)
        db_obj = DBHandler()
        userDoesntExist = db_obj.create_user(user)
        if not userDoesntExist:
            return make_response(jsonify({'message': 'user already exists'}), 400)
        else:
            return make_response(jsonify({'message': 'new user created'}), 201)


class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']

        email = str(email)
        password = str(password)

        if not empty_string_catcher(email)or not empty_string_catcher(password):
            return make_response(jsonify({'message': 'please fill all fields'}), 400)

        if not isString(email) or not isString(password):
            return make_response(jsonify({'message': 'please insert correct values'}), 400)

        if not email_validator(email):
            return make_response(jsonify({'message': 'malformed email'}), 400)

        db_obj = DBHandler()
        user = db_obj.auth_user(email, password)
        if user is None:
            return make_response(jsonify({'message': 'user does not exist'}), 400)

        if not check_password_hash(user['password'], password):
            return make_response(jsonify({'message': 'user does not exist'}), 400)

        access_token = create_access_token(identity=user)
        return make_response(jsonify({'token': access_token}), 200)


class Logout(Resource):
    def post(self):
        pass


api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
