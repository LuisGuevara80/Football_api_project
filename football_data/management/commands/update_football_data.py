from django.core.management.base import BaseCommand
from football_data.updaters import DataUpdater
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update football data from API'

    def handle(self, *args, **options):
        # Initialize the DataUpdater
        updater = DataUpdater()

        try:
            # Log the start of the update process
            logger.info("Starting football data update...")
            
            # Call the method to update all data
            updater.update_all_data()
            
            # If successful, print a success message to the console
            self.stdout.write(self.style.SUCCESS('Successfully completed football data update'))
            
            # Print the total number of API calls made during the update
            self.stdout.write(f"Total API calls made: {updater.api_calls}")
        
        except Exception as e:
            # If an error occurs, print an error message to the console
            self.stdout.write(self.style.ERROR(f"An error occurred during the update process: {str(e)}"))
            
            # Also log the error for debugging purposes
            logger.error(f"An error occurred during the update process: {str(e)}")
        
        finally:
            # Log the end of the update process, regardless of success or failure
            logger.info("Update process finished.")