from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Test environment variables'

    def handle(self, *args, **kwargs):
        # Print the value of FOOTBALL_API_KEY from settings
        self.stdout.write(f"FOOTBALL_API_KEY: {settings.FOOTBALL_API_KEY}")

        # Print the value of DEBUG from settings
        self.stdout.write(f"DEBUG: {settings.DEBUG}")

        # Print the first 5 characters of SECRET_KEY from settings
        # Only showing part of the key for security reasons
        self.stdout.write(f"SECRET_KEY: {settings.SECRET_KEY[:5]}...")