import time
import random
import requests
import logging
from django.conf import settings
from django.core.cache import cache
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class FootballApiClient:
    # Base URL for the API
    BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"
    
    def __init__(self):
        # Set up headers for API requests
        self.headers = {
            "X-RapidAPI-Key": settings.FOOTBALL_API_KEY,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        self.api_calls = 0  # Counter for API calls

    def make_request(self, endpoint, params=None):
        # Generate a unique cache key based on the endpoint and parameters
        cache_key = hashlib.md5(f"{endpoint}_{str(params)}".encode()).hexdigest()
        
        # Check if the response is cached
        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response

        url = f"{self.BASE_URL}/{endpoint}"
        
        retries = 0
        for i in range(5):  # Try up to 5 times
            try:
                # Make the API request
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                self.api_calls += 1

                data = response.json()
                # Cache the response for 1 hour
                cache.set(cache_key, data, 3600)
                
                if retries > 0:
                    logger.info(f"Request succeeded after {retries} retries for endpoint: {endpoint}")
                
                return data
            except requests.exceptions.RequestException as e:
                retries += 1
                # Exponential backoff with a small random delay
                wait_time = 2 ** i + random.uniform(0, 1)
                logger.warning(f"Request failed (attempt {retries}). Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
        
        # Log error if all retries fail
        logger.error(f"Failed to get response after {retries} retries for endpoint: {endpoint}")
        raise Exception(f"Failed to get response after {retries} retries for endpoint: {endpoint}")

    # Methods for specific API endpoints
    def get_countries(self):
        return self.make_request("countries")

    def get_leagues(self):
        return self.make_request("leagues")

    def get_teams(self, league, season):
        params = {"league": league, "season": season}
        return self.make_request("teams", params)

    def get_team_info(self, team_id):
        params = {"id": team_id}
        return self.make_request("teams", params)

    def get_players(self, team, season, page=1):
        params = {"team": team, "season": season, "page": page}
        return self.make_request("players", params)

    def get_fixtures(self, date):
        params = {"date": date}
        return self.make_request("fixtures", params)