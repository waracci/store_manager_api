from flask_bcrypt import Bcrypt


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
