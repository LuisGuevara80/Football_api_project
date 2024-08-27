from .models import League

def leagues_processor(request):
    """
    Context processor to add top leagues to all templates.

    This function retrieves the top 5 leagues based on predefined IDs and
    makes them available globally in all templates.
    """
    # Filter League objects based on specific IDs
    # '39': Premier League
    # '140': La Liga
    # '78': Bundesliga
    # '135': Serie A
    # '61': Ligue 1
    leagues = League.objects.filter(id__in=['39', '140', '78', '135', '61'])

    # Return a dictionary with the 'global_leagues' key
    # This will be merged into the context of all templates
    return {'global_leagues': leagues}