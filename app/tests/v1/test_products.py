import unittest
from flask import json
from app import create_app


class TestProduct(unittest.TestCase):
    """Tests for Product endpoints"""

    def setUp(self):
        """Set up Testing configuration and environments"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.product_data = {
                            "product_name": "cake",
                            "product_description": "sweet and lovely",
                            "product_quantity": 5,
                            "product_category": "bakery",
                            "product_moq": 100
                        }

    def user_authentication_register(self, email="mail@mail.com", password="pass", confirm_password="pass"):
        """Method to register a User"""
        user_register = {
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'role': 'admin'
        }
        return self.client().post('/api/v1/register', data=user_register)

    def user_authentication_login(self, email="mail@mail.com", password="pass"):
        """Method to login a User"""
        user_login = {
            'email': email,
            'password': password
        }
        return self.client().post('/api/v1/login', data=user_login)

    def test_post_product(self):
        """Test that Admin can add a product"""

        # Authenticate User
        self.user_authentication_register(email="mail1234@mail.com", password="pass", confirm_password="pass")
        response = self.user_authentication_login(email="mail1234@mail.com", password="pass")

        authentication_token = json.loads(response.data.decode())['access_token']

        product_posted = self.client().post(
            '/api/v1/products',
            headers=dict(Authorization="Bearer {}".format(authentication_token)),
            data=self.product_data)
        result = json.loads(product_posted.data.decode())
        self.assertEqual(result['message'], 'success')
        self.assertEqual(product_posted.status_code, 201)

    # def test_fetch_all_products(self):
    #     """Test that a user can fetch all products"""

    #     # Authenticate User
    #     self.user_authentication_register(email="mailxx@mail.com", password="pass", confirm_password="pass")
    #     response = self.user_authentication_login(email="mailxx@mail.com", password="pass")

    #     authentication_token = json.loads(response.data.decode())['access_token']

    #     product_posted = self.client().post(
    #         '/api/v1/products',
    #         headers=dict(Authorization="Bearer {}".format(authentication_token)),
    #         data=self.product_data)
    #     result = json.loads(product_posted.data.decode())
    #     self.assertEqual(result['message'], 'success')
    #     self.assertEqual(product_posted.status_code, 201)

    #     fetch_product = self.client().get(
    #         '/api/v1/products',
    #         headers=dict(Authorization="Bearer {}".format(authentication_token)))
    #     self.assertEqual(fetch_product.status_code, 200)

    # def test_fetch_single_product(self):
    #     """Test user can fetch specific product using the product's id"""

    #     # Authenticate User
    #     self.user_authentication_register(email="ulbricht@mail.com", password="pass", confirm_password="pass")
    #     response = self.user_authentication_login(email="ulbricht@mail.com", password="pass")

    #     authentication_token = json.loads(response.data.decode())['access_token']

    #     product_posted = self.client().post(
    #         '/api/v1/products',
    #         headers=dict(Authorization="Bearer {}".format(authentication_token)),
    #         data=self.product_data)
    #     result = json.loads(product_posted.data.decode())
    #     self.assertEqual(product_posted.status_code, 201)

    #     fetch_single_product = self.client().get(
    #         '/api/v1/products/{}'.format(result['product']['product_id']),
    #         headers=dict(Authorization="Bearer {}".format(authentication_token)))
    #     self.assertEqual(fetch_single_product.status_code, 200)

    def tearDown(self):
        """Empty the products and clear the data"""
        self.product_data = {}
