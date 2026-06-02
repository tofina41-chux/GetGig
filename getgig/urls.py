from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from projects import views as project_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
    
    # Core Landing Page Mapping
    path('', project_views.landing_page, name='home'),
    
    # Progressive Web App Configuration URLs
    path('', include('pwa.urls')),
    
    # Standard authentication views helper
    path('accounts/', include('django.contrib.auth.urls')), 
]

# Media handling fallback rules
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Ensure Vercel can serve legacy local assets if Cloudinary is bypassed
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)