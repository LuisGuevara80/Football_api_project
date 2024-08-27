import random
import time
import logging
from django.utils import timezone
from django.utils.timezone import localtime
from django.db import transaction
from .models import Country, League, Season, Team, Player, Fixture, Venue
from .api_client import FootballApiClient

logger = logging.getLogger(__name__)

class DataUpdater:
    def __init__(self):
        self.client = FootballApiClient()
        # Dictionary of top leagues and their associated team IDs
        self.top_leagues = {
            '39': ['33', '34', '40', '42', '46', '47', '48', '49', '50', '51'],  # Premier League
            '140': ['529', '530', '531', '532', '533', '536', '537', '538', '540', '541'],  # La Liga
            '78': ['157', '159', '161', '162', '163', '164', '165', '167', '168', '169'],  # Bundesliga
            '135': ['489', '492', '494', '496', '497', '498', '499', '500', '502', '503'],  # Serie A
            '61': ['77', '79', '80', '81', '82', '83', '84', '85', '91', '93']  # Ligue 1
        }
        self.api_calls = 0
        self.max_api_calls = 95  # Safety margin to avoid exceeding API limit

    @transaction.atomic
    def update_all_data(self):
        # Main method to update all data, runs different updates based on the day of the week
        logger.info("Starting data update...")
        
        try:
            current_time = localtime(timezone.now())
            day_of_week = current_time.weekday()
            logger.info(f"Current day of week: {day_of_week} (Current time: {current_time})")
            
            self.update_fixtures()  # Daily update
            
            if day_of_week == 0:  # Monday
                logger.info("It's Monday. Updating countries and leagues.")
                self.update_countries_and_leagues()
            
            if day_of_week < 5:  # Monday to Friday
                logger.info(f"Updating teams and players for day {day_of_week}.")
                self.update_teams_and_players(day_of_week)
            
            if day_of_week == 5:  # Saturday
                logger.info("It's Saturday. Updating venues.")
                self.update_venues()
            
            self.clean_old_data()
            
            logger.info(f"Data update completed. Total API calls: {self.api_calls}")
        except Exception as e:
            logger.error(f"Error during data update: {str(e)}")

    def update_countries_and_leagues(self):
        # Updates country and league data
        logger.info("Updating countries and leagues...")
        try:
            # Fetch and update countries
            countries_data = self.client.get_countries()
            self.api_calls += 1
            
            for country in countries_data['response']:
                Country.objects.update_or_create(
                    name=country['name'],
                    defaults={
                        'code': country.get('code'),
                        'flag_url': country.get('flag'),
                        'last_updated': timezone.now()
                    }
                )
            
            # Fetch and update leagues
            leagues_data = self.client.get_leagues()
            self.api_calls += 1
            
            for league in leagues_data['response']:
                if str(league['league']['id']) in self.top_leagues:
                    country, _ = Country.objects.get_or_create(name=league['country']['name'])
                    League.objects.update_or_create(
                        id=league['league']['id'],
                        defaults={
                            'name': league['league']['name'],
                            'type': league['league'].get('type', 'Unknown'),
                            'country': country,
                            'logo_url': league['league'].get('logo'),
                            'last_updated': timezone.now()
                        }
                    )
            
            logger.info(f"Countries and leagues updated. API calls: {self.api_calls}")
        except Exception as e:
            logger.error(f"Error updating countries and leagues: {str(e)}")

    def update_fixtures(self):
        # Updates fixture data for the previous day
        logger.info("Updating fixtures...")
        yesterday = (timezone.now() - timezone.timedelta(days=1)).strftime("%Y-%m-%d")
        try:
            fixtures_data = self.client.get_fixtures(yesterday)
            self.api_calls += 1
            logger.info(f"Retrieved {len(fixtures_data['response'])} fixtures for {yesterday}")
            
            fixtures_created = 0
            for fixture in fixtures_data['response']:
                if str(fixture['league']['id']) not in self.top_leagues:
                    continue  # Skip fixtures for leagues we're not interested in

                try:
                    # Create or update league, teams, and season
                    league, _ = League.objects.get_or_create(
                        id=fixture['league']['id'],
                        defaults={
                            'name': fixture['league']['name'],
                            'country': Country.objects.get_or_create(name=fixture['league']['country'])[0],
                            'type': 'Unknown',
                            'last_updated': timezone.now()
                        }
                    )
                    home_team, _ = Team.objects.get_or_create(
                        id=fixture['teams']['home']['id'],
                        defaults={
                            'name': fixture['teams']['home']['name'],
                            'national': False,
                            'country': Country.objects.get_or_create(name=fixture['teams']['home'].get('country', 'Unknown'))[0]
                        }
                    )
                    away_team, _ = Team.objects.get_or_create(
                        id=fixture['teams']['away']['id'],
                        defaults={
                            'name': fixture['teams']['away']['name'],
                            'national': False,
                            'country': Country.objects.get_or_create(name=fixture['teams']['away'].get('country', 'Unknown'))[0]
                        }
                    )
                    
                    season, _ = Season.objects.get_or_create(
                        year=fixture['league']['season'],
                        league=league,
                        defaults={
                            'start_date': timezone.now().date(),
                            'end_date': timezone.now().date() + timezone.timedelta(days=365),
                            'current': True
                        }
                    )
                    
                    # Create or update fixture
                    Fixture.objects.update_or_create(
                        id=fixture['fixture']['id'],
                        defaults={
                            'referee': fixture['fixture'].get('referee'),
                            'date': fixture['fixture']['date'],
                            'timestamp': fixture['fixture']['timestamp'],
                            'status_short': fixture['fixture']['status']['short'],
                            'league': league,
                            'season': season,
                            'round': fixture['league']['round'],
                            'team_home': home_team,
                            'team_away': away_team,
                            'goals_home': fixture['goals']['home'],
                            'goals_away': fixture['goals']['away'],
                            'last_updated': timezone.now()
                        }
                    )
                    fixtures_created += 1
                except Exception as e:
                    logger.error(f"Error updating fixture: {str(e)}")
            logger.info(f"Fixtures updated. Created/Updated: {fixtures_created}. API calls: {self.api_calls}")
        except Exception as e:
            logger.error(f"Error updating fixtures: {str(e)}")

    def update_teams_and_players(self, day_index):
        # Updates team and player data, spreading the updates over the week
        logger.info("Updating teams and players...")
        teams_updated = 0
        
        start_index = day_index * 2
        end_index = start_index + 2
        
        for league_id, team_ids in self.top_leagues.items():
            if self.api_calls >= self.max_api_calls:
                logger.warning("Approaching API call limit. Stopping update.")
                return
            
            logger.info(f"Updating teams for league {league_id}")
            
            for team_id in team_ids[start_index:end_index]:
                try:
                    # Fetch and update team data
                    team_data = self.client.get_team_info(team_id)
                    self.api_calls += 1
                    
                    if not team_data['response']:
                        logger.warning(f"No data found for team {team_id}")
                        continue
                    
                    team_info = team_data['response'][0]['team']
                    
                    country, _ = Country.objects.get_or_create(name=team_info.get('country', 'Unknown'))
                    team_obj, created = Team.objects.update_or_create(
                        id=team_info['id'],
                        defaults={
                            'name': team_info['name'],
                            'code': team_info.get('code'),
                            'country': country,
                            'founded': team_info.get('founded'),
                            'national': team_info.get('national', False),
                            'logo_url': team_info.get('logo'),
                            'last_updated': timezone.now()
                        }
                    )
                    
                    teams_updated += 1
                    logger.info(f"{'Created' if created else 'Updated'} team: {team_obj.name}")
                    
                    self.update_team_players(team_obj)
                except Exception as e:
                    logger.error(f"Error updating team {team_id}: {str(e)}")
        
        logger.info(f"Total teams updated: {teams_updated}")

    def update_team_players(self, team_obj):
        # Updates player data for a specific team
        logger.info(f"Updating players for team {team_obj.name}")
        players_created = 0
        players_updated = 0
        for page in range(1, 5):  # 4 pages of players
            if self.api_calls >= self.max_api_calls:
                logger.warning("Approaching API call limit. Stopping player update.")
                return
            
            try:
                time.sleep(random.uniform(1, 3))  # Random delay to avoid API rate limiting
                
                players_data = self.client.get_players(team=team_obj.id, season=timezone.now().year, page=page)
                self.api_calls += 1
                logger.info(f"Retrieved players for team {team_obj.name}, page {page}")
                
                if not players_data['response']:
                    break
                
                for player in players_data['response']:
                    player_info = player['player']
                    player_obj, created = Player.objects.update_or_create(
                        id=player_info['id'],
                        defaults={
                            'name': player_info['name'],
                            'firstname': player_info.get('firstname'),
                            'lastname': player_info.get('lastname'),
                            'age': player_info.get('age'),
                            'birth_date': player_info.get('birth', {}).get('date'),
                            'nationality': player_info.get('nationality'),
                            'height': player_info.get('height'),
                            'weight': player_info.get('weight'),
                            'photo_url': player_info.get('photo'),
                            'team': team_obj,
                            'last_updated': timezone.now()
                        }
                    )
                    if created:
                        players_created += 1
                    else:
                        players_updated += 1
            except Exception as e:
                logger.error(f"Error updating players for team {team_obj.name}, page {page}: {str(e)}")
                break
        logger.info(f"Created {players_created} and updated {players_updated} players for team {team_obj.name}")

    def update_venues(self):
        # Updates venue data for the top 10 teams in each of the 5 main leagues
        logger.info("Starting venue update for the top 10 teams in each of the 5 main leagues...")
        venues_updated = 0
        
        for league_id, team_ids in self.top_leagues.items():
            if self.api_calls >= self.max_api_calls:
                logger.warning("Approaching API call limit. Stopping venue update.")
                return
            
            logger.info(f"Updating venues for league {league_id}")
            
            for team_id in team_ids:
                if self.api_calls >= self.max_api_calls:
                    logger.warning("Approaching API call limit. Stopping venue update.")
                    return

                logger.info(f"Attempting to update venue for team {team_id}")
                try:
                    team_obj = Team.objects.get(id=team_id)
                except Team.DoesNotExist:
                    logger.warning(f"Team with id {team_id} does not exist in the database. Skipping venue update.")
                    continue

                try:
                    team_data = self.client.get_team_info(team_id)
                    self.api_calls += 1
                    
                    if not team_data['response']:
                        logger.warning(f"No data found for team {team_id}")
                        continue
                    
                    venue_info = team_data['response'][0]['venue']
                    
                    venue_obj, created = Venue.objects.update_or_create(
                        id=venue_info['id'],
                        defaults={
                            'name': venue_info['name'],
                            'address': venue_info.get('address'),
                            'city': venue_info.get('city'),
                            'capacity': venue_info.get('capacity'),
                            'surface': venue_info.get('surface'),
                            'image_url': venue_info.get('image'),
                            'team': team_obj,
                            'last_updated': timezone.now()
                        }
                    )
                    
                    venues_updated += 1
                    logger.info(f"{'Created' if created else 'Updated'} venue: {venue_obj.name} for team {team_obj.name}")
                except Exception as e:
                    logger.error(f"Error updating venue for team {team_id}: {str(e)}")
        
        logger.info(f"Total venues updated: {venues_updated}")
        if venues_updated == 0:
            logger.warning("No venues were updated. This may indicate an issue.")
        elif venues_updated < len(self.top_leagues) * 10:
            logger.warning(f"Only {venues_updated} venues were updated out of {len(self.top_leagues) * 10} expected. Some updates may have failed.")

    def clean_old_data(self):
        # Removes data older than 7 days to keep the database clean
        logger.info("Cleaning old data...")
        try:
            seven_days_ago = timezone.now() - timezone.timedelta(days=7)
            Team.objects.filter(last_updated__lt=seven_days_ago).delete()
            Player.objects.filter(last_updated__lt=seven_days_ago).delete()
            logger.info("Old data cleaned.")
        except Exception as e:
            logger.error(f"Error cleaning old data: {str(e)}")