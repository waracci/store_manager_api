import unittest
from flask import json
from app import create_app


class TestSales(unittest.TestCase):
    """Tests for Sales endpoints"""

    def setUp(self):
        """Test environment setup"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.sales_data = {
                            "made_by": "James",
                            "cart": [],
                            "cart_price": 500
                          }

    def user_authentication_register(self, email="mail@mail.com", password="pass", confirm_password="pass"):
        """Method to register a User"""
        user_register = {
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        }
        return self.client().post('/api/v1/register', data=user_register)

    def user_authentication_login(self, email="mail@mail.com", password="pass"):
        """Method to login a User"""
        user_login = {
            'email': email,
            'password': password
        }
        return self.client().post('/api/v1/login', data=user_login)

    def test_post_sales(self):
        """Test that an attendant can make a sale"""

        # Authenticate User
        self.user_authentication_register()
        response = self.user_authentication_login()

        authentication_token = json.loads(response.data.decode())['access_token']

        sale_made = self.client().post(
            '/api/v1/sales',
            headers=dict(Authorization="Bearer {}".format(authentication_token)),
            data=self.sales_data)
        result = json.loads(sale_made.data.decode())
        self.assertEqual(sale_made.status_code, 201)
        self.assertEqual(result['message'], 'success')

    def test_fetch_all_sales(self):
        """Test that Admin can fetch all sales records"""

        # Authenticate User
        self.user_authentication_register()
        response = self.user_authentication_login()

        authentication_token = json.loads(response.data.decode())['access_token']

        sale_made = self.client().post(
            '/api/v1/sales',
            headers=dict(Authorization="Bearer {}".format(authentication_token)),
            data=self.sales_data)
        result = json.loads(sale_made.data.decode())
        self.assertEqual(result['message'], 'success')
        fetch_sales = self.client().get(
            '/api/v1/sales')
        self.assertEqual(fetch_sales.status_code, 200)

    def test_single_sales_record(self):
        """Test that Admin/Attendant can fetch single record"""

        # Authenticate User
        self.user_authentication_register()
        response = self.user_authentication_login()

        authentication_token = json.loads(response.data.decode())['access_token']

        sale_made = self.client().post(
            '/api/v1/sales',
            headers=dict(Authorization="Bearer {}".format(authentication_token)),
            data=self.sales_data)
        result = json.loads(sale_made.data.decode())

        fetch_sales_record = self.client().get(
            '/api/v1/sales/{}'.format(result['sales']['id']))
        self.assertEqual(fetch_sales_record.status_code, 200)

    def tearDown(self):
        """Empty the sales and clear data"""
        self.sales_data = {}
