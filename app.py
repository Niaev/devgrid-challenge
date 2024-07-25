"""uWSGI executable app"""

# Main Flask app import
from index import app as application

# Environment variables import
from config import *

if __name__ == '__main__':
    application.run(
        debug=DEBUG
    )