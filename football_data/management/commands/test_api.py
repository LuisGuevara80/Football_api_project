from django.core.management.base import BaseCommand
import requests
from django.conf import settings

class Command(BaseCommand):
    help = 'Test API connection'

    def handle(self, *args, **kwargs):
        # API endpoint for testing connection
        url = "https://api-football-v1.p.rapidapi.com/v3/timezone"
        
        # Headers required for API authentication
        headers = {
            "X-RapidAPI-Key": settings.FOOTBALL_API_KEY,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        
        # Make a GET request to the API
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print success message in green
            self.stdout.write(self.style.SUCCESS('Successfully connected to the API'))
            # Print the API response
            self.stdout.write(f"Response: {response.json()}")
        else:
            # Print error message in red if connection failed
            self.stdout.write(self.style.ERROR(f'Failed to connect to the API. Status code: {response.status_code}'))