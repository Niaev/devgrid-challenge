"""MongoDB consumer class"""

# General imports
from datetime import datetime

# MongoDB imports
from pymongo import MongoClient

# Environment variables
from config import *

class MDBConsumer:
    """Inserts, updates and reads data into/from MongoDB"""

    def __init__(self, port=MDB_PORT):
        self.db = MongoClient(MDB_HOST, port)
        self.cli = self.db[MDB_DB]
        self.collection = self.cli[MDB_CL]
        self.collection.create_index('user_id', unique=True)
    
    def insert_new_request(self, uid: str) -> None:
        """Insert new request into collection with given user ID"""
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        item = {
            'user_id': uid,
            'datetime': date,
            'weather_data': []
        }
        self.collection.insert_one(item)

    def push_weather_data(self, uid: str, weather_data: dict) -> None:
        """Push weather data into collection item with given user ID"""
        self.collection.update_one(
            {'user_id': uid},
            {'$push': {'weather_data': weather_data}}
        )

    def pull_len_weather_data(self, uid: str) -> int:
        """Get the length of weather data collected by given user ID"""
        data = self.collection.find_one({'user_id': uid})
        if type(data) == type(None):
            return -1
        return len(data['weather_data'])

    def close(self) -> None:
        """Close connection"""
        self.db.close()