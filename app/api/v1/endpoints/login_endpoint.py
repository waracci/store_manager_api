"""Login endpoint [POST]"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify
from validate_email import validate_email

from ..models.User import User

api = Namespace('User Login',
                description='User login')

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

        is_valid = validate_email(email)
        if not is_valid:
            return make_response(jsonify({'message': 'enter a valid email',
                                          'status': 'failed'}), 400)

        if password == None:
            return make_response(jsonify({'message': 'incomplete credentials provided. Please try again',
                                              'status': 'failed'}), 401)

        if User.password == '':
            return make_response(jsonify({'message': 'Invalid email or password. Please try again',
                                              'status': 'failed'}), 401)
        # Fetch user by email to check if user exists
        existing_user = User.get_single_user(email)
        if email and existing_user == 'not found':
            return make_response(jsonify({'message': 'Unknown email. Please sign up',
                                              'status': 'failed'}), 401)

        try:
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
