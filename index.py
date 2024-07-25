"""Flask app base file"""

# Web development imports
from flask import Flask
from flask_cors import CORS

# Environment variables
from config import *

# Initialize Flask app
app = Flask(__name__)
CORS(app) # Enable CORS for Flask app

from routes import * 

# Development server execution
if __name__ == '__main__':
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )