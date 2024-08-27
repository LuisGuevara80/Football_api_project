from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from django.utils import timezone
from datetime import datetime, timedelta
from .models import League, Team, Player, Fixture, Country
from django.db.models import Q, Prefetch
from django.core.paginator import Paginator
from django.http import JsonResponse

def home(request):
    """
    Render the home page with featured leagues and recent fixtures.
    """
    # Get the 5 most recent leagues
    leagues = League.objects.all()[:5]

    # Calculate date range for fixtures (3 days ago to now)
    now = timezone.now()
    date_from = now - timedelta(days=3)
    date_to = now 
    
    # Get the 10 most recent fixtures within the date range
    latest_fixtures = Fixture.objects.filter(
        date__range=(date_from, date_to)
    ).order_by('date')[:10]  
    
    context = {
        'leagues': leagues,
        'latest_fixtures': latest_fixtures,
        'now': now,
    }
    return render(request, 'football_data/home.html', context)

def leagues(request):
    """
    Display a list of all leagues with search functionality.
    """
    search_query = request.GET.get('search', '')
    leagues = League.objects.all()

    # Filter leagues if search query is provided
    if search_query:
        leagues = leagues.filter(name__icontains=search_query)

    context = {
        'leagues': leagues,
        'search_query': search_query,
    }
    return render(request, 'football_data/leagues.html', context)

def league_detail(request, league_id):
    """
    Display details of a specific league.
    """
    league = get_object_or_404(League, id=league_id)
    teams = Team.objects.filter(country=league.country)
    context = {
        'league': league,
        'teams': teams,
    }
    return render(request, 'football_data/league_detail.html', context)

def teams(request):
    """
    Display a list of teams with search and filter functionality.
    """
    search_query = request.GET.get('search', '')
    league_filter = request.GET.get('league', '')
    
    teams = Team.objects.select_related('country').all()
    leagues = League.objects.all()

    # Apply filters if provided
    if search_query:
        teams = teams.filter(name__icontains=search_query)
    
    if league_filter:
        teams = teams.filter(country__league__id=league_filter)

    # Set up pagination
    paginator = Paginator(teams, 12)  
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    default_logo_url = static('img/default_team_v3.png')

    # Handle AJAX requests for infinite scrolling
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        team_data = []
        for team in page_obj:
            league = League.objects.filter(country=team.country).first()
            team_data.append({
                'id': team.id,
                'name': team.name,
                'logo_url': team.logo_url or default_logo_url,
                'country': team.country.name,
                'league': league.name if league else 'N/A'
            })
        return JsonResponse({'teams': team_data, 'has_next': page_obj.has_next()})

    context = {
        'page_obj': page_obj,
        'leagues': leagues,
        'search_query': search_query,
        'selected_league': league_filter,
        'default_logo_url': default_logo_url,
    }
    return render(request, 'football_data/teams.html', context)

def team_detail(request, team_id):
    """
    Display details of a specific team.
    """
    team = get_object_or_404(Team.objects.select_related('country', 'venue'), id=team_id)
    players = Player.objects.filter(team=team)
    
    # Try to get the league of the team
    try:
        league = League.objects.get(country=team.country)
    except League.DoesNotExist:
        league = None

    context = {
        'team': team,
        'players': players,
        'league': league,
    }
    return render(request, 'football_data/team_detail.html', context)

def players(request):
    """
    Display a list of players with search and filter functionality.
    """
    search_query = request.GET.get('search', '')
    league_filter = request.GET.get('league', '')
    team_filter = request.GET.get('team', '')
    
    players = Player.objects.all()
    leagues = League.objects.all()
    teams = Team.objects.all()

    # Apply filters if provided
    if search_query:
        players = players.filter(name__icontains=search_query)
    
    if league_filter:
        teams_in_league = Team.objects.filter(country__league__id=league_filter)
        players = players.filter(team__in=teams_in_league)
        teams = teams.filter(country__league__id=league_filter)
    
    if team_filter:
        players = players.filter(team__id=team_filter)

    # Set up pagination
    paginator = Paginator(players, 20)  
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Handle AJAX requests for infinite scrolling
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        player_data = [{
            'id': player.id,
            'name': player.name,
            'team': player.team.name,
            'photo_url': player.photo_url or '/static/football_data/img/default_player.png',
        } for player in page_obj]
        return JsonResponse({'players': player_data, 'has_next': page_obj.has_next()})

    context = {
        'page_obj': page_obj,
        'leagues': leagues,
        'teams': teams,
        'search_query': search_query,
        'selected_league': league_filter,
        'selected_team': team_filter,
    }
    return render(request, 'football_data/players.html', context)

def player_detail(request, player_id):
    """
    Display details of a specific player.
    """
    player = get_object_or_404(Player, id=player_id)
    context = {
        'player': player,
    }
    return render(request, 'football_data/player_detail.html', context)

def fixtures(request):
    """
    Display a list of fixtures with date and league filtering.
    """
    selected_date = request.GET.get('date', timezone.now().date())
    selected_league = request.GET.get('league', '')

    # Convert string date to datetime object if necessary
    if isinstance(selected_date, str):
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.now().date()

    fixtures = Fixture.objects.filter(date__date=selected_date)
    if selected_league:
        fixtures = fixtures.filter(league__id=selected_league)

    # Optimize query by selecting related fields
    fixtures = fixtures.select_related('league', 'team_home', 'team_away', 'season')

    # Format the round for each fixture
    for fixture in fixtures:
        fixture.formatted_round = format_round(fixture.round)

    leagues = League.objects.all()

    context = {
        'fixtures': fixtures,
        'leagues': leagues,
        'selected_date': selected_date,
        'selected_league': selected_league,
    }

    return render(request, 'football_data/fixtures.html', context)

def format_round(round_string):
    """
    Format the round string for better readability.
    """
    if round_string.startswith("Regular Season"):
        parts = round_string.split('-')
        if len(parts) > 1:
            return f"Jornada {parts[1].strip()}"
    elif round_string.lower().startswith("round"):
        return f"Ronda {round_string.split()[-1]}"
    return round_string

def search(request):
    """
    Perform a global search across leagues, teams, and players.
    """
    query = request.GET.get('q', '')
    leagues = League.objects.filter(name__icontains=query)
    teams = Team.objects.filter(name__icontains=query)
    players = Player.objects.filter(name__icontains=query)
    
    context = {
        'query': query,
        'leagues': leagues,
        'teams': teams,
        'players': players,
    }
    return render(request, 'football_data/search.html', context)