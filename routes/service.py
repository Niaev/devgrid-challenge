"""Must contain all service endpoints"""

# General imports
import aiohttp
import asyncio
from time import sleep

# MongoDB imports
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError

# Flask app import
from index import app

# Project imports
from classes.MDBConsumer import MDBConsumer
from classes.OpenWeatherConsumer import OWConsumer

@app.get('/test/')
def test_app():
    """Test if service is running"""
    return {
        'message': 'Running ok!'
    }, 200

@app.get('/collect/<uid>') # Comment this before finishing
@app.post('/collect/<uid>')
async def collect_and_store(uid: str):
    """Collect data from OpenWeather API and store on MongoDB"""

    # Initialize MongoDB consumer
    try:
        mdbc = MDBConsumer()
    except ServerSelectionTimeoutError:
        # In case of Mongo Server out of service
        # Return HTTP error 500
        return {
            'message': 'Database out of service!'
        }, 500

    try:
        # Insert current request with no weather data
        mdbc.insert_new_request(uid)
    except DuplicateKeyError:
        # In case of existing user ID, return message below
        # With HTTP error 400
        mdbc.close() # Close Mongo connection
        return {
            'message': 'User ID already in use!'
        }, 400

    # Initialize OpenWeather API consumer
    owc = OWConsumer(mdbc)
    # Get list of cities IDs
    cities_ids = owc.cities_ids

    # Handle batches to respect API request limit for free accounts
    limit = 60
    n = len(cities_ids)
    n_batches = round(n / limit) # Number of needed batches
    len_batches = round(n / n_batches) # Maximum length of each batch
    # Create batches
    cities_ids_batches = []
    for i in range(n_batches):
        j = i + 1
        # Define minimum and maximum positions
        min_pos = i * len_batches
        max_pos = j * len_batches
        # Add batch
        cities_ids_batches.append(cities_ids[min_pos:max_pos])

    # Prepare asynchronous session
    async with aiohttp.ClientSession() as session:
        # Do concurrent requests for each batch of cities IDs
        for batch in cities_ids_batches:
            tasks = [owc.get_data_and_store(session, uid, city) for city in batch]
            _ = await asyncio.gather(*tasks)
            # Wait one minute
            sleep(60)

    mdbc.close() # Close Mongo connection

    # Successful return
    return {
        'message': 'Success!'
    }, 200

@app.get('/progress/<uid>')
def check_collection_progress(uid: str):
    """Check data collection and storage progress"""

    # Initialize MongoDB consumer
    try:
        mdbc = MDBConsumer()
    except ServerSelectionTimeoutError:
        # In case of Mongo Server out of service
        # Return HTTP error 500
        return {
            'message': 'Database out of service!'
        }, 500

    # Initialize OpenWeather API consumer
    owc = OWConsumer(mdbc)
    # Get list of cities IDs
    cities_ids = owc.cities_ids

    # Total number of cities IDs
    n = len(cities_ids)
    # Number of concluded requests
    n_concluded = mdbc.pull_len_weather_data(uid)

    # If there is no value for given user ID
    if n_concluded == -1:
        mdbc.close() # Close Mongo connection
        return {
            'message': 'User ID doesn\'t exist!'
        }, 400

    # Calculate percentage of conclusion
    percentage = round(n_concluded / n, 2) * 100

    mdbc.close() # Close Mongo connection

    # Successful return
    return {
        'message': 'Success!',
        'percentage': f'{percentage}%'
    }, 200