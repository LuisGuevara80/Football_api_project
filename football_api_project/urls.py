from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Define main URL patterns for the project
urlpatterns = [
    ##--------------------------------------------------------------------------##
    ##---------------------------------Admin------------------------------------##
    path('admin/', admin.site.urls),
    
    ##--------------------------------------------------------------------------##
    ##---------------------------------football_data----------------------------##
    path('', include('football_data.urls')),
]

# Serve static and media files during development
if settings.DEBUG:
    # Static files (CSS, JavaScript, Images)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Media files (Uploaded content)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)