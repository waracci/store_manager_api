"""Register endpoint [POST]"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify
from validate_email import validate_email

from ..models.User import User

api = Namespace('User registration endpoint',
                description='User registration endpoint')

parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')
parser.add_argument('confirm_password')


@api.route('')
class RegistrationEndpoint(Resource):
    """Endpoint for User registration"""

    def post(self):
        """Create new user"""

        args = parser.parse_args()
        email = args['email']
        password = args['password']
        confirm_password = args['confirm_password']

        is_valid = validate_email(email)
        if not is_valid:
            return make_response(jsonify({'message': 'enter a valid email',
                                          'status': 'failed'}), 400)

        if password == '' or password == ' ':
            return make_response(jsonify({'message': 'enter password',
                                          'status': 'failed'}), 401)

        # Compare passwords
        if password != confirm_password:
            return make_response(jsonify({'message': 'passwords do not match',
                                          'status': 'failed'}), 401)

        # Check for existing registration of email provided
        existing_user = User.get_single_user(email)

        if existing_user == 'not found':
            try:
                # Register new User
                new_user = User(email, password)
                new_user.save_user()

                success_registration = {
                    'message': 'Registration success. Please sign in.',
                    'status': 'ok'
                }
                return make_response(jsonify(success_registration), 201)
            except Exception as exception_msg:
                return make_response(jsonify({'message': str(exception_msg),
                                              'status': 'failed'}), 401)
        else:
            return make_response(jsonify({'message': 'User exists. Please sign in',
                                          'status': 'failed'}), 202)
