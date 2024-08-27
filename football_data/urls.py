from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# Define URL patterns for the football_data app
urlpatterns = [
    ##--------------------------------------------------------------------------##
    ##---------------------------------Home-------------------------------------##
    path('', views.home, name='home'),
    
    ##--------------------------------------------------------------------------##
    ##---------------------------------Leagues----------------------------------##
    path('leagues/', views.leagues, name='leagues'),
    path('leagues/<int:league_id>/', views.league_detail, name='league_detail'),
    
    ##--------------------------------------------------------------------------##
    ##---------------------------------Teams------------------------------------##
    path('teams/', views.teams, name='teams'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    
    ##--------------------------------------------------------------------------##
    ##---------------------------------PLayers----------------------------------##
    path('players/', views.players, name='players'),
    path('players/<int:player_id>/', views.player_detail, name='player_detail'),
    
    ##--------------------------------------------------------------------------##
    ##---------------------------------Fixtures---------------------------------##
    path('fixtures/', views.fixtures, name='fixtures'),
    
    ##--------------------------------------------------------------------------##
    ##---------------------------------Search-----------------------------------##
    path('search/', views.search, name='search'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)