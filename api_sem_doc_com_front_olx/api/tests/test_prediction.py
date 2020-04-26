import unittest
import os
import json
from app import create_app

class RegressionModelOLXTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.request_object = {
                        'trade_price_last1': '129.08900',
                        'curve_based_price': '127.561201',
                        'curve_based_price_last1': '129.435587',
                        'is_callable': '0',
                        'bond_id': '348003',
                        }

    def test_api_can_make_prediction(self):
        """Test API can make prediction"""
        res = self.client().post('/prediction/', data=self.request_object)
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        pass

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
