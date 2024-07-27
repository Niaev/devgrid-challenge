"""Test Flask app cases"""

# General imports
import unittest

# Faker imports 
from faker import Faker

# Project imports 
from index import app
from classes.MDBConsumer import MDBConsumer

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        self.fake = Faker()
        self.new_uid = str(self.fake.random_int())
        self.unused_uid = str(self.fake.random_int())
        self.context = app.app_context()
        self.context.push()
        self.client = app.test_client()
        self.mdbc = MDBConsumer()

    def tearDown(self):
        self.context.pop()
        self.mdbc.collection.delete_one({'user_id': self.new_uid})
        self.mdbc.close()

    def test_test(self):
        """Test the test route"""
        response = self.client.get('/test/')
        
        expected_status = 200
        response_status = response.status_code
        self.assertEqual(
            expected_status,
            response_status,
            'Not the expected status'
        )

        expected_data = {
            'message': 'Running ok!'
        }
        response_data = response.json
        self.assertEqual(
            expected_data['message'],
            response_data['message'],
            'Not the expected response'
        )
    
    def test_successful_collect(self):
        """Test successful collect route case"""
        response = self.client.post(f'/collect/{self.new_uid}')
        
        expected_status = 200
        response_status = response.status_code
        self.assertEqual(
            expected_status,
            response_status,
            'Not the expected status'
        )

        expected_data = {
            'message': 'Success!'
        }
        response_data = response.json
        self.assertEqual(
            expected_data['message'],
            response_data['message'],
            'Not the expected response'
        )
    
    def test_failed_collect(self):
        """Test failed collect route case"""
        response = self.client.post(f'/collect/{self.new_uid}')

        response = self.client.post(f'/collect/{self.new_uid}')

        expected_status = 400
        response_status = response.status_code
        self.assertEqual(
            expected_status,
            response_status,
            'Not the expected status'
        )

        expected_data = {
            'message': 'User ID already in use!'
        }
        response_data = response.json
        self.assertEqual(
            expected_data['message'],
            response_data['message'],
            'Not the expected response'
        )

    def test_successful_progress(self):
        """Test successful progress route case"""
        response = self.client.post(f'/collect/{self.new_uid}')
        response = self.client.get(f'/progress/{self.new_uid}')

        expected_status = 200
        response_status = response.status_code
        self.assertEqual(
            expected_status,
            response_status,
            'Not the expected status'
        )

        expected_data = {
            'message': 'Success!'
        }
        response_data = response.json
        self.assertEqual(
            expected_data['message'],
            response_data['message'],
            'Not the expected response message'
        )
        self.assertIn(
            'percentage',
            response_data,
            'Not the expected response: don\'t have percentage'
        )

    def test_failed_progress(self):
        """Test failed progress route case"""
        response = self.client.get(f'/progress/{self.new_uid}')

        expected_status = 400
        response_status = response.status_code
        self.assertEqual(
            expected_status,
            response_status,
            'Not the expected status'
        )

        expected_data = {
            'message': 'User ID doesn\'t exist!'
        }
        response_data = response.json
        self.assertEqual(
            expected_data['message'],
            response_data['message'],
            'Not the expected response message'
        )