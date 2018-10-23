"""Login endpoint [POST]"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify
from validate_email import validate_email

from ..models.User import User
from ..utils.validator import AuthDataTransferObject

api = AuthDataTransferObject.authentication_namespace

authentication_validator_register = AuthDataTransferObject.authentication_model_register
authentication_validator_login = AuthDataTransferObject.authentication_model_login

parser = reqparse.RequestParser()

# Registration data
parser.add_argument('email', required=True, help='Email cannot be blank')
parser.add_argument('password', required=True, help='Password cannot be blank')
parser.add_argument('confirm_password')
parser.add_argument('role')


@api.route('register')
class RegistrationEndpoint(Resource):
    """Endpoint for User registration"""

    @api.doc('User registration endpoint')
    @api.expect(authentication_validator_register)
    def post(self):
        """Create new user"""

        args = parser.parse_args()
        email = args['email']
        password = args['password']
        confirm_password = args['confirm_password']
        role = args['role']

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
        
        if role == '' or role == ' ':
            return make_response(jsonify({'message': 'User role required',
                                          'status': 'failed'}), 401)

        # Check for existing registration of email provided
        existing_user = User.get_single_user(email)

        if existing_user == 'not found':
            try:
                # Register new User
                new_user = User(email, password, role)
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

@api.route('login')
class LoginEndpoint(Resource):
    """Endpoint for User Login"""

    @api.expect(authentication_validator_login)
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
