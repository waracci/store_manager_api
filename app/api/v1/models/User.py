from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from instance.config import secret_key


class User:
    """User class contains user constructor and authentication methods"""

    # Class variable to save registered users
    registered_users = []

    def __init__(self, email, password):
        """Initialize User Object with an email and password"""

        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def validate_user_password(self, password):
        """Compare the user entered password and user registered password"""

        return Bcrypt().check_password_hash(self.password, password)

    def save_user(self):
        """Save User Object to Datastructure (dictionary)"""

        new_user = dict(
            email=self.email,
            password=self.password
        )

        User.registered_users.append(new_user)
        return new_user

    def generate_auth_token(self, user_id):
        """method to generate access token"""

        # Set up payload with an expiration time
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(
                payload,
                secret_key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

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