"""Open Weather API consumer class"""

# General imports
import aiohttp
import asyncio

# Project imports
from classes.MDBConsumer import MDBConsumer

# Environment variables
from config import *

class OWConsumer:
    """Consume API"""

    def __init__(self, mdbc: MDBConsumer):
        with open('data/cities.txt', 'r') as f:
            cities = f.read().split(', ')
        
        self.cities_ids = cities
        self.mdbc = mdbc
    
    async def get_data_and_store(self, 
                                 session: aiohttp.ClientSession, 
                                 uid: str,
                                 city_id: str) -> None:
        """Receive asynchronous session, user ID and city ID to collect data and store"""
        url = f'https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric'
        async with session.get(url, timeout=30) as response:
            raw_data = await response.json()
            weather_data = {
                'city_id': city_id,
                'temperature_celsius': raw_data['main']['temp'],
                'humidity': raw_data['main']['humidity']
            }

            self.mdbc.push_weather_data(uid, weather_data)