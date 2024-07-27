"""Test OpenWeather API consumer cases"""

# General imports
import unittest
import asyncio

# Asynchronous stuff imports
import aiohttp

# Faker imports
from faker import Faker

# Test subject imports
from classes.MDBConsumer import MDBConsumer
from classes.OpenWeatherConsumer import OWConsumer

class OWCTest(unittest.TestCase):

    def setUp(self):
        self.fake = Faker()
        self.existing_uid = str(self.fake.random_int())
        self.nonexisting_uid = str(self.fake.random_int())
        self.mdbc = MDBConsumer()
        self.owc = OWConsumer(self.mdbc)   
        self.cities = self.owc.cities_ids[:5]
        self.timeout = aiohttp.ClientTimeout(total=60)

    def tearDown(self):
        self.mdbc.collection.delete_one({'user_id': self.existing_uid})
        self.mdbc.close()
    
    async def test_successful_get_store(self):
        """Test data retrieval and storage with existing user ID"""
        self.mdbc.insert_new_request(self.existing_uid)
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            tasks = [self.owc.get_data_and_store(session, self.existing_uid, city) for city in self.cities]
            _ = await asyncio.gather(*tasks)
        
        expected = 5
        actual = self.mdbc.pull_len_weather_data(self.existing_uid)
        self.assertEqual(
            expected,
            actual,
            'Value from pull differ from expected'
        )

    async def test_failed_get_store(self):
        """Test data retrieval and storage with non-existing user ID"""
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            tasks = [self.owc.get_data_and_store(session, self.existing_uid, city) for city in self.cities]
            _ = await asyncio.gather(*tasks)
        
        expected = -1
        actual = self.mdbc.pull_len_weather_data(self.existing_uid)
        self.assertEqual(
            expected,
            actual,
            'Value from pull differ from expected'
        )