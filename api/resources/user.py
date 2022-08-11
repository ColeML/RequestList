from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_restful import abort, Resource, reqparse
from hmac import compare_digest

from api.models.user import UserModel
from api.db import jwt_redis_blocklist
from api.config import Config


_create_user_parser = reqparse.RequestParser()
_create_user_parser.add_argument('username', type=str, required=True, help='Username Required.')
_create_user_parser.add_argument('password', type=str, required=True, help='Password Required.')
_create_user_parser.add_argument('first_name', type=str, required=True, help='First Name Required')
_create_user_parser.add_argument('last_name', type=str, required=True, help='Last Name Required')
_create_user_parser.add_argument('email', type=str, required=True, help='Email Required')

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help='Username Required.')
_user_parser.add_argument('password', type=str, required=True, help='Password Required.')


class UserRegister(Resource):
    def post(self) -> (dict, int):
        data = _create_user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            abort(400, message=f"A user with username {data['username']} already exists.")

        user = UserModel(**data)
        user.save_to_db()

        return {'message': "User created successfully."}, 201


class User(Resource):
    @classmethod
    @jwt_required()  # TODO Remove the get method
    def get(cls, user_id) -> (dict, int):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message='User not found.')
        return user.json(), 200

    @classmethod
    @jwt_required(refresh=True)
    def delete(cls, user_id) -> (dict, int):
        user_id = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User deleted.'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls) -> (dict, int):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if not user or not compare_digest(user.password, data['password']):
            abort(401, message='Invalid credentials')

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {'access_token': access_token, 'refresh_token': refresh_token}, 200


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls) -> (dict, int):
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=Config.ACCESS_EXPIRES)
        return {'message': "User logged out."}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self) -> (dict, int):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
