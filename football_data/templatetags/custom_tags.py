from django import template
from football_data.models import League
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def default_static(value, default_path):
    """
    Custom template tag to provide a fallback for static files.

    This tag checks if the provided value is empty or only whitespace.
    If so, it returns a static file path using the provided default_path.
    Otherwise, it returns the original value.
    """
    if value and value.strip():
        return value
    return static(default_path)

@register.simple_tag
def get_league_name(country):
    """
    Custom template tag to get the name of a league for a given country.

    This tag queries the League model to find a league associated with
    the provided country. If found, it returns the league's name.
    If not found, it returns 'N/A'.
    """
    league = League.objects.filter(country=country).first()
    return league.name if league else 'N/A'