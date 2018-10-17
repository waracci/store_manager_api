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

    def test_post_product(self):
        """Test that Admin can add a product"""

        product_posted = self.client().post(
            '/api/v1/products',
            data=self.product_data)
        result = json.loads(product_posted.data.decode())
        self.assertEqual(result['message'], 'success')
        self.assertEqual(product_posted.status_code, 201)

    def test_fetch_all_products(self):
        """Test that a user can fetch all products"""

        product_posted = self.client().post(
            '/api/v1/products',
            data=self.product_data)
        result = json.loads(product_posted.data.decode())
        self.assertEqual(product_posted.status_code, 201)

        fetch_product = self.client().get(
            '/api/v1/products')
        self.assertEqual(fetch_product.status_code, 200)

    def test_fetch_single_product(self):
        """Test user can fetch specific product using the product's id"""

        product_posted = self.client().post(
            '/api/v1/products',
            data=self.product_data)
        result = json.loads(product_posted.data.decode())
        self.assertEqual(product_posted.status_code, 201)

        fetch_single_product = self.client().get(
            '/api/v1/products/{}'.format(result['product']['product_id']))
        self.assertEqual(fetch_single_product.status_code, 200)

    def tearDown(self):
        """Empty the products and clear the data"""
        self.product_data = {}
