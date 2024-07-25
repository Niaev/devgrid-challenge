"""MongoDB consumer class"""

# General imports
from datetime import datetime

# MongoDB imports
from pymongo import MongoClient
##from pymongo.errors import DuplicateKeyError

# Environment variables
from config import *

class MDBConsumer:
    """Inserts, updates and reads data into/from MongoDB"""

    def __init__(self):
        self.db = MongoClient(MDB_HOST, MDB_PORT)
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

    