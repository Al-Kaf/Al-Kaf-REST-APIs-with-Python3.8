import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="the name is required ")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="the password is required ")

    def post(self):
        request_data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(request_data['username']):
            return {"massage": "the user name is already exists"}, 400

        user = UserModel(**request_data)
        user.save_to_db()

        return {"massage": "User created successfully."}, 201




