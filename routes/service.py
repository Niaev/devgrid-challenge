"""Must contain all service endpoints"""

# General imports
import aiohttp
import asyncio

# MongoDB imports
from pymongo.errors import DuplicateKeyError

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
    }

@app.get('/collect/<uid>')
@app.post('/collect/<uid>')
async def collect_and_store(uid: str):
    """Collect data from OpenWeather API and store on MongoDB"""

    mdbc = MDBConsumer()
    try:
        mdbc.insert_new_request(uid)
    except DuplicateKeyError:
        return {
            'message': 'User ID already in use!'
        }, 400

    owc = OWConsumer(mdbc)
    cities_ids = owc.cities_ids[:59]

    async with aiohttp.ClientSession() as session:
        tasks = [owc.get_data_and_store(session, uid, city) for city in cities_ids]

        results = await asyncio.gather(*tasks)

    return {
        'message': 'Success!'
    }, 200

@app.get('/progress/<uid>')
def check_collection_progress(uid: str):
    """Check data collection and storage progress"""
    return None