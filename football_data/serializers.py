from rest_framework import serializers
from .models import Country, League, Season, Team, Player, Fixture

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'flag_url', 'continent', 'last_updated']

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['id', 'name', 'type', 'country', 'country_code', 'logo_url', 'last_updated']

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['year', 'start_date', 'end_date', 'current', 'league', 'last_updated']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'country', 'league', 'code', 'founded', 'logo_url', 'venue_name', 'venue_capacity', 'last_updated']

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'firstname', 'lastname', 'date_of_birth', 'nationality', 'height', 'weight', 'team', 'position', 'market_value', 'last_updated']

class FixtureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fixture
        fields = ['id', 'api_fixture_id', 'league', 'season', 'round', 'date', 'status', 'home_team', 'away_team', 'home_score', 'away_score', 'home_score_halftime', 'away_score_halftime', 'home_score_fulltime', 'away_score_fulltime', 'referee', 'time_zone', 'venue', 'last_updated']