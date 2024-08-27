from django.core.management.base import BaseCommand
from football_data.api_client import FootballApiClient
from django.utils import timezone
import logging
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test API calls for the new update strategy'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = FootballApiClient()
        self.start_time = datetime.now()
        # Dictionary of top leagues and their associated team IDs
        self.top_leagues = {
            '39': ['33', '34', '40', '42', '46', '47', '48', '49', '50', '51'],  # Premier League
            '140': ['529', '530', '531', '532', '533', '536', '537', '538', '540', '541'],  # La Liga
            '78': ['157', '159', '161', '162', '163', '164', '165', '167', '168', '169'],  # Bundesliga
            '135': ['489', '492', '494', '496', '497', '498', '499', '500', '502', '503'],  # Serie A
            '61': ['77', '79', '80', '81', '82', '83', '84', '85', '91', '93']  # Ligue 1
        }

    def add_arguments(self, parser):
        # Add optional argument to simulate a specific day of the week
        parser.add_argument('--day', type=int, help='Day of the week to simulate (0-6, where 0 is Monday)')

    def log_progress(self, message):
        # Helper method to log progress with elapsed time
        elapsed_time = datetime.now() - self.start_time
        self.stdout.write(f"[{elapsed_time}] {message}")

    def handle(self, *args, **options):
        # Main method to handle the command execution
        simulated_day = options['day'] if options['day'] is not None else timezone.now().weekday()
        self.log_progress(f"Starting API test for new update strategy (Simulating day: {simulated_day})...")

        self.test_fixtures(simulated_day)  # Daily update

        if simulated_day == 0:  # Monday
            self.test_countries_and_leagues()

        if simulated_day < 5:  # Monday to Friday
            self.test_teams_and_players(simulated_day)

        if simulated_day == 5:  # Saturday
            self.test_venues()

        self.log_progress(self.style.SUCCESS('API test completed successfully'))
        self.log_progress(f"Total API calls made: {self.client.api_calls}")

    def test_countries_and_leagues(self):
        # Test API calls for countries and leagues (weekly update)
        self.log_progress("\nTesting countries and leagues calls (weekly update)...")
        countries_data = self.client.get_countries()
        self.log_progress(f"Retrieved {len(countries_data['response'])} countries")
        
        leagues_data = self.client.get_leagues()
        self.log_progress(f"Retrieved {len(leagues_data['response'])} leagues")
        self.log_progress(f"API calls: {self.client.api_calls}")

    def test_teams_and_players(self, day_index):
        # Test API calls for teams and players (daily update, Monday to Friday)
        self.log_progress(f"\nTesting teams and players update for day {day_index}...")
        season = timezone.now().year
        start_index = day_index * 2
        end_index = start_index + 2

        for league_id, team_ids in self.top_leagues.items():
            self.log_progress(f"\nTesting league {league_id}")
            
            for team_id in team_ids[start_index:end_index]:
                self.log_progress(f"Testing team {team_id}")
                team_data = self.client.get_team_info(team_id)
                self.log_progress(f"Retrieved info for team {team_id}")
                
                for page in range(1, 5):  # Test 4 pages of players
                    players_data = self.client.get_players(team_id, season, page)
                    self.log_progress(f"Retrieved players for team {team_id}, page {page}")
                    self.log_progress(f"API calls: {self.client.api_calls}")
                    
                    if not players_data['response']:
                        break
                    
                    if self.client.api_calls >= 95:
                        self.log_progress(self.style.WARNING('Approaching API call limit. Stopping test.'))
                        return
                    
                    time.sleep(2)  # Add a 2-second delay between requests

    def test_fixtures(self, simulated_day):
        # Test API calls for fixtures (daily update)
        self.log_progress("\nTesting fixtures call...")
        simulated_date = timezone.now() - timedelta(days=1)
        simulated_date = simulated_date - timedelta(days=(simulated_date.weekday() - simulated_day) % 7)
        fixtures_data = self.client.get_fixtures(simulated_date.strftime("%Y-%m-%d"))
        self.log_progress(f"Retrieved {len(fixtures_data['response'])} fixtures for {simulated_date.strftime('%Y-%m-%d')}")
        self.log_progress(f"API calls: {self.client.api_calls}")

        if fixtures_data['response']:
            sample_fixture = fixtures_data['response'][0]
            self.log_progress(f"Sample fixture: {sample_fixture['fixture']['id']} - {sample_fixture['teams']['home']['name']} vs {sample_fixture['teams']['away']['name']}")
        else:
            self.log_progress("No fixtures found for this date.")

    def test_venues(self):
        # Test API calls for venues (weekly update, Saturday)
        self.log_progress("\nTesting venues update...")
        
        for league_id, team_ids in self.top_leagues.items():
            self.log_progress(f"\nTesting venues for league {league_id}")
            
            for team_id in team_ids:
                self.log_progress(f"Testing venue for team {team_id}")
                team_data = self.client.get_team_info(team_id)
                self.log_progress(f"Retrieved team info (including venue) for team {team_id}")
                self.log_progress(f"API calls: {self.client.api_calls}")
                
                if self.client.api_calls >= 95:
                    self.log_progress(self.style.WARNING('Approaching API call limit. Stopping test.'))
                    return
                
                time.sleep(2)  # Add a 2-second delay between requests