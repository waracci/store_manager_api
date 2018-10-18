"""Login endpoint [POST]"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify

from ..models.User import User

api = Namespace('User Login',
                description='User login functionality')

parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')


@api.route('')
class LoginEndpoint(Resource):
    """Endpoint for User Login"""

    def post(self):
        """login existing user"""

        args = parser.parse_args()
        email = args['email']
        password = args['password']

        try:
            # Fetch user by email to check if user exists
            existing_user = User.get_single_user(email)
            if existing_user and User.validate_user_password(password):
                # Generate access token
                authentication_token = User.generate_auth_token(existing_user['email'])
                if authentication_token:
                    return make_response(jsonify({'message': 'login success',
                                                  'status': 'ok',
                                                  'access_token': authentication_token.decode()}), 200)
            else:
                return make_response(jsonify({'message': 'Invalid email or password. Please try again',
                                              'status': 'failed'}), 401)
        except Exception as exception_msg:
            return make_response(jsonify({'message': str(exception_msg),
                                          'status': 'failed'}), 500)
