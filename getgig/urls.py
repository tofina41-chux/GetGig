from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from projects import views as project_views

urlpatterns = [
    # Core Landing Page Mapping (Fixes the root 404!)
    path('', project_views.landing_page, name='home'),
    
    # App Routes
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
    
    # Progressive Web App URLs
    path('', include('pwa.urls')),
    
    # Standard authentication views helper
    path('accounts/', include('django.contrib.auth.urls')), 
]

# Ensure static & media routing rules apply during local development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)