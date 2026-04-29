from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
    path('', RedirectView.as_view(pattern_name='users:dashboard_redirect', permanent=False)),
    # This adds the login/logout views automatically
    path('accounts/', include('django.contrib.auth.urls')), 
    path('', RedirectView.as_view(pattern_name='users:dashboard_redirect', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)