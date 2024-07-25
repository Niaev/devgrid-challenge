"""Environment variables configuration with python-dotenv"""

# General imports
import os

# Environment variables handler import
from dotenv import load_dotenv
load_dotenv()

# Renaming function for ease of use 
env = os.getenv

# Service hostname and port
HOST=env('HOST')
PORT=env('PORT')

# MongoDB hostname and port
MDB_HOST=env('MDB_HOST')
MDB_PORT=env('MDB_PORT')
# MongoDB database and collection
MDB_DB=env('MDB_DB')
MDB_CL=env('MDB_CL')

# Development stuff
DEBUG=bool(int(env('DEBUG')))