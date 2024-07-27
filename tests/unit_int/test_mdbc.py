"""Test MongoDB consumer cases"""

# General imports
import unittest

# MongoDB imports
from pymongo.errors import DuplicateKeyError

# Faker imports
from faker import Faker

# Test subject imports
from classes.MDBConsumer import MDBConsumer

class MDBCTest(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()
        self.existing_uid = str(self.fake.random_int())
        self.nonexisting_uid = str(self.fake.random_int())
        self.mdbc = MDBConsumer()
    
    def tearDown(self):
        self.mdbc.collection.delete_one({'user_id': self.existing_uid})
        self.mdbc.close()

    def test_successful_insert(self):
        """Test inserting new request with a new user ID"""
        self.mdbc.insert_new_request(self.existing_uid)
    
    def test_failed_insert(self):
        """Test inserting new request with existing user ID"""
        self.mdbc.insert_new_request(self.existing_uid)

        self.assertRaises(
            DuplicateKeyError,
            self.mdbc.insert_new_request,
            self.existing_uid
        )

    def test_successful_push(self):
        """Test pushing weather data to existing user ID"""
        self.mdbc.insert_new_request(self.existing_uid)

        self.mdbc.push_weather_data(
            self.existing_uid,
            {
                'city_id': str(self.fake.random_int()),
                'temperature_celsius': self.fake.random_int(),
                'humidity': self.fake.random_int()
            }
        )

    def test_failed_push(self):
        """Test pushing weather data to non-existing user ID"""
        self.mdbc.push_weather_data(
            self.nonexisting_uid,
            {
                'city_id': str(self.fake.random_int()),
                'temperature_celsius': self.fake.random_int(),
                'humidity': self.fake.random_int()
            }
        )
    
    def test_successful_pull(self):
        """Test retrieving lenght of weather data from existing user ID"""
        self.mdbc.insert_new_request(self.existing_uid)

        self.mdbc.push_weather_data(
            self.existing_uid,
            {
                'city_id': str(self.fake.random_int()),
                'temperature_celsius': self.fake.random_int(),
                'humidity': self.fake.random_int()
            }
        )
        
        expected = 1
        actual = self.mdbc.pull_len_weather_data(self.existing_uid)
        self.assertEqual(
            expected,
            actual,
            'Value from pull differ from expected'
        )

    def test_failed_pull(self):
        """Test retrieving lenght of weather data from non-existing user ID"""
        expected = -1
        actual = self.mdbc.pull_len_weather_data(self.nonexisting_uid)
        self.assertEqual(
            expected,
            actual,
            'Value from pull differ from expected'
        )