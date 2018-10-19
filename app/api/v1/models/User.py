from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from instance.config import secret_key


class User:
    """User class contains user constructor and authentication methods"""

    # Class variable to save registered users
    registered_users = []
    password = ''

    def __init__(self, email, password):
        """Initialize User Object with an email and password"""

        self.email = email
        User.password = Bcrypt().generate_password_hash(password).decode()

    @classmethod
    def validate_user_password(cls, password):
        """Compare the user entered password and user registered password"""

        return Bcrypt().check_password_hash(User.password, password)

    def save_user(self):
        """Save User Object to Datastructure (dictionary)"""

        new_user = dict(
            email=self.email,
            password=self.password
        )

        User.registered_users.append(new_user)

    @staticmethod
    def get_single_user(email):
        """Retrieve user details by email"""

        single_user = [user for user in User.registered_users if user['email'] == email]
        if single_user:
            return single_user[0]
        return 'not found'

    @classmethod
    def generate_auth_token(cls, email):
        """method to generate access token"""

        # Set up payload with an expiration time
        try:
            payload = {
                'exp': datetime.now() + timedelta(days=1, seconds=5),
                'iat': datetime.now(),
                'sub': email
            }

            return jwt.encode(
                payload,
                secret_key,
                algorithm='HS256'
            )
        except Exception as exception_msg:
            return exception_msg

    @staticmethod
    def decode_auth_token(authentication_token):
        """method to decode the authentication token"""

        try:
            payload = jwt.decode(authentication_token, secret_key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please sign in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please sign in again'

    def __repr__(self):
        return "<User '{}'>".format(self.email)
