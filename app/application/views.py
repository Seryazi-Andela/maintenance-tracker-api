from . import apcn_v1
from .models import UserRequest
from ..app_utils.utils import empty_string_catcher, isString, isInteger, isBool
from ..database.db_handler import DBHandler

from flask_restful import Resource, Api, reqparse
from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Api(apcn_v1)


class MakeRequests(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        logged_in_user = current_user['username']
        logged_in_user_isadmin = current_user['isadmin']

        if logged_in_user_isadmin:
            return make_response(jsonify({'message': 'admin can not make a request'}), 400)

        data = request.get_json()
        header = data['header']
        details = data['details']
        approved = data['approved']
        resolved = data['resolved']

        username = logged_in_user

        if not isString(username)or not isString(header)or not isString(details)or not isBool(approved)or not isBool(resolved):
            return make_response(jsonify({'message': 'please insert correct values'}), 400)

        if not empty_string_catcher(username) or not empty_string_catcher(header) or not empty_string_catcher(details):
            return make_response(jsonify({'message': 'please fill all fields'}), 400)

        user_req = UserRequest(username, header, details, approved, resolved)
        db_obj = DBHandler()
        db_obj.create_request(user_req)

        return make_response(jsonify({'message': 'new request created'}), 201)

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        username = current_user['username']

        db_obj = DBHandler()
        response = db_obj.get_user_requests(username)
        if len(response) <= 0:
            return make_response(jsonify({'message': 'no such entry found'}), 400)

        return make_response(jsonify({'message': response}), 200)


class ManageUserRequest(Resource):
    @jwt_required
    def get(self, requestid):
        current_user = get_jwt_identity()
        username = current_user['username']

        db_obj = DBHandler()
        response = db_obj.get_user_request(username, requestid)
        if response is None:
            return make_response(jsonify({'message': 'no such entry found'}), 400)

        return make_response(jsonify({'message': response}), 200)

    @jwt_required
    def put(self, requestid):
        current_user = get_jwt_identity()
        username = current_user['username']

        data = request.get_json()
        header = data['header']
        details = data['details']
        if not empty_string_catcher(details) or not empty_string_catcher(header):
            return make_response(jsonify({'message': 'please enter a value'}), 400)

        db_obj = DBHandler()
        response = db_obj.modify_user_request(
            header, details, username, requestid)
        if response is None:
            return make_response(jsonify({'message': 'no such entry found'}), 400)

        return make_response(jsonify({'message': response}), 200)


api.add_resource(MakeRequests, '/requests')
api.add_resource(ManageUserRequest, '/requests/<string:requestid>')
