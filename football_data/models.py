from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
##--------------------------------------------------------------------------##
##----------------------------------Country----------------------------------##
"""
    Represents a country in the football database.
    
    This model stores information about countries, including their name,
    country code, and flag URL. It's used to associate teams, leagues,
    and players with their respective countries.
"""
class Country(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    code = models.CharField(max_length=3, null=True, blank=True)
    flag_url = models.URLField(null=True, blank=True)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def truncate_old_data(cls):
        yesterday = timezone.now() - timezone.timedelta(days=1)
        cls.objects.filter(last_updated__lt=yesterday).delete()
##--------------------------------------------------------------------------##
##----------------------------------League----------------------------------##
"""
    Represents a football league or competition.
    
    This model stores information about leagues, including their name,
    type (e.g., league, cup), associated country, and the seasons in which
    they operate. It's used to categorize fixtures and teams.
"""
class League(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    type = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    logo_url = models.URLField()
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['country', 'name']

    def __str__(self):
        return f"{self.name} ({self.country.name})"

    @classmethod
    def truncate_old_data(cls):
        yesterday = timezone.now() - timezone.timedelta(days=1)
        cls.objects.filter(last_updated__lt=yesterday).delete()
##--------------------------------------------------------------------------##
##----------------------------------Season----------------------------------##
"""
    Represents a football season.
    
    This model stores information about individual seasons, including
    the year, start and end dates, and whether it's the current season.
    It's used to associate leagues and fixtures with specific time periods.
"""
class Season(models.Model):
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    current = models.BooleanField(default=False)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='seasons')
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.year} - {self.league.name}"

    @classmethod
    def truncate_old_data(cls):
        yesterday = timezone.now() - timezone.timedelta(days=1)
        cls.objects.filter(last_updated__lt=yesterday).delete()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('End date must be after start date.')

##--------------------------------------------------------------------------##
##-----------------------------------Team-----------------------------------##
"""
    Represents a football team.
    
    This model stores detailed information about teams, including their name,
    country, founding year, and venue details. It's used to associate players
    and fixtures with specific teams.
"""
class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(max_length=3, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    founded = models.IntegerField(null=True, blank=True)
    national = models.BooleanField(default=False)
    logo_url = models.URLField()
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def truncate_old_data(cls):
        yesterday = timezone.now() - timezone.timedelta(days=1)
        cls.objects.filter(last_updated__lt=yesterday).delete()

    def clean(self):
        if self.founded and self.founded < 1800:
            raise ValidationError('Founded year must be 1800 or later.')
        if self.venue_capacity and self.venue_capacity < 0:
            raise ValidationError('Venue capacity must be a positive number.')
##--------------------------------------------------------------------------##
##----------------------------------Venue-----------------------------------##
"""
    Represents a venue or stadium in the football database.
    
    This model stores detailed information about individual venues,
    including their name, location, capacity, and associated team.
    It's used to track information about the locations where matches
    are played and provides additional context for fixtures and teams.
"""
class Venue(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100)
    capacity = models.IntegerField(null=True, blank=True)
    surface = models.CharField(max_length=50)
    image_url = models.URLField()
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='venue')
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def truncate_old_data(cls):
        yesterday = timezone.now() - timezone.timedelta(days=1)
        cls.objects.filter(last_updated__lt=yesterday).delete()
##--------------------------------------------------------------------------##
##----------------------------------Player----------------------------------##
"""
    Represents a football player.
    
    This model stores detailed information about individual players,
    including personal details, physical attributes, and their current team.
    It's used to track player information and associations.
"""
class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=100, null=True, blank=True)
    birth_country = models.CharField(max_length=100, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    height = models.CharField(max_length=10, null=True, blank=True)
    weight = models.CharField(max_length=10, null=True, blank=True)
    injured = models.BooleanField(null=True, blank=True)
    photo_url = models.URLField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['lastname', 'firstname']

    def __str__(self):
        return f"{self.name} ({self.team.name})"

    @classmethod
    def truncate_old_data(cls):
        yesterday = timezone.now() - timezone.timedelta(days=1)
        cls.objects.filter(last_updated__lt=yesterday).delete()

    def clean(self):
        if self.height and not self.height.isdigit():
            raise ValidationError('Height must be a numeric value.')
        if self.weight and not self.weight.isdigit():
            raise ValidationError('Weight must be a numeric value.')
##--------------------------------------------------------------------------##
##---------------------------------Fixture----------------------------------##
"""
    Represents a football match or fixture.
    
    This model stores detailed information about individual matches,
    including the teams involved, scores, status, and various other
    match-specific details. It's the central model for tracking game data.
"""
class Fixture(models.Model):
    id = models.IntegerField(primary_key=True)
    referee = models.CharField(max_length=100, null=True, blank=True)
    time_zone = models.CharField(max_length=50)
    date = models.DateTimeField(db_index=True)
    timestamp = models.IntegerField()
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, related_name='fixtures')
    status_long = models.CharField(max_length=50)
    status_short = models.CharField(max_length=2)
    status_elapsed = models.IntegerField(null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='fixtures')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='fixtures')
    round = models.CharField(max_length=50)
    team_home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_fixtures')
    team_away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_fixtures')
    goals_home = models.IntegerField(null=True, blank=True)
    goals_away = models.IntegerField(null=True, blank=True)
    score_halftime_home = models.IntegerField(null=True, blank=True)
    score_halftime_away = models.IntegerField(null=True, blank=True)
    score_fulltime_home = models.IntegerField(null=True, blank=True)
    score_fulltime_away = models.IntegerField(null=True, blank=True)
    score_extratime_home = models.IntegerField(null=True, blank=True)
    score_extratime_away = models.IntegerField(null=True, blank=True)
    score_penalty_home = models.IntegerField(null=True, blank=True)
    score_penalty_away = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.team_home.name} vs {self.team_away.name} - {self.date}"

    def is_finished(self):
        return self.status_short in ['FT', 'AET', 'PEN']

    def clean(self):
        if self.home_score is not None and self.home_score < 0:
            raise ValidationError('Home score cannot be negative.')
        if self.away_score is not None and self.away_score < 0:
            raise ValidationError('Away score cannot be negative.')