"""Must contain all service endpoints"""

# General imports
import asyncio

# Flask app import
from index import app

@app.get('/test/')
def test_app():
    """Test if service is running"""
    return {
        'message': 'Running ok!'
    }

@app.post('/collect/<uid>')
async def collect_and_store(uid: str):
    """Collect data from OpenWeather API and store on MongoDB"""
    return None

@app.get('/progress/<uid>')
def check_collection_progress(uid: str):
    """Check data collection and storage progress"""
    return None