"""Register endpoint [POST]"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify

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

        # Compare passwords
        if password != confirm_password:
            return make_response(jsonify({'message': 'passwords do not match',
                                          'status': 'failed'}), 401)

        # Check for existing registration of email provided
        existing_user = User.get_single_user(self, email)

        if not existing_user:
            try:
                # Register new User
                new_user = User(email, password)
                new_user.save_user()

                success_registration = {
                    'message': 'Registration success. Please sign in.',
                    'status': 'ok'
                }
                return make_response(jsonify(success_registration), 200)
            except Exception as e:
                return make_response(jsonify({'message': str(e),
                                              'status': 'failed'}), 401)
        else:
            return make_response(jsonify({'message': 'User exists. Please sign in',
                                          'status': 'failed'}), 202)
