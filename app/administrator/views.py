from . import admin_v1
from ..application.models import UserRequest
from ..app_utils.utils import empty_string_catcher, isString, isInteger
from ..database.db_handler import DBHandler

from flask_restful import Resource, Api, reqparse
from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Api(admin_v1)


class GetAllRequests(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        isadmin = current_user['isadmin']

        if not isadmin:
            return make_response(jsonify({'message': 'user not authorised'}), 401)

        db_obj = DBHandler()
        response = db_obj.get_all_user_requests()
        return make_response(jsonify({'message': response}), 200)


class ApproveUserRequest(Resource):
    @jwt_required
    def put(self, requestid):
        current_user = get_jwt_identity()
        isadmin = current_user['isadmin']

        if not isadmin:
            return make_response(jsonify({'message': 'user not authorised'}), 401)

        db_obj = DBHandler()
        response = db_obj.approve_user_request(requestid)
        if response is None:
            return make_response(jsonify({'message': 'could not find entry to modify'}), 400)

        return make_response(jsonify({'message': response}), 201)


class DisapproveUserRequest(Resource):
    @jwt_required
    def put(self, requestid):
        current_user = get_jwt_identity()
        isadmin = current_user['isadmin']

        if not isadmin:
            return make_response(jsonify({'message': 'user not authorised'}), 401)

        db_obj = DBHandler()
        response = db_obj.disapprove_user_request(requestid)
        if response is None:
            return make_response(jsonify({'message': 'could not find entry to modify'}), 400)

        return make_response(jsonify({'message': response}), 201)


class ResolveUserRequest(Resource):
    @jwt_required
    def put(self, requestid):
        current_user = get_jwt_identity()
        isadmin = current_user['isadmin']

        if not isadmin:
            return make_response(jsonify({'message': 'user not authorised'}), 401)

        db_obj = DBHandler()
        isApproved = db_obj.check_approval(requestid)
        if not isApproved:
            return make_response(jsonify({'message': 'request must be approved before resolving'}), 400)

        response = db_obj.resolve_user_request(requestid)
        if response is None:
            return make_response(jsonify({'message': 'could not find entry to modify'}), 400)

        return make_response(jsonify({'message': response}), 201)


api.add_resource(GetAllRequests, '/requests')
api.add_resource(ApproveUserRequest, '/requests/<int:requestid>/approve')
api.add_resource(DisapproveUserRequest, '/requests/<int:requestid>/disapprove')
api.add_resource(ResolveUserRequest, '/requests/<int:requestid>/resolve')
