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

    def test_post_sales(self):
        """Test that an attendant can make a sale"""

        sale_made = self.client().post(
            '/api/v1/sales',
            data=self.sales_data)
        result = json.loads(sale_made.data.decode())
        self.assertEqual(sale_made.status_code, 201)
        self.assertEqual(result['message'], 'success')

    def test_fetch_all_sales(self):
        """Test that Admin can fetch all sales records"""

        sale_made = self.client().post(
            '/api/v1/sales',
            data=self.sales_data)
        result = json.loads(sale_made.data.decode())

        fetch_sales = self.client().get(
            '/api/v1/sales')
        self.assertEqual(fetch_sales.status_code, 200)

    def test_single_sales_record(self):
        """Test that Admin/Attendant can fetch single record"""

        sale_made = self.client().post(
            '/api/v1/sales',
            data=self.sales_data)
        result = json.loads(sale_made.data.decode())

        fetch_sales_record = self.client().get(
            '/api/v1/sales/{}'.format(result['sales']['id']))
        self.assertEqual(fetch_sales_record.status_code, 200)

    def tearDown(self):
        """Empty the sales and clear data"""
        self.sales_data = {}
