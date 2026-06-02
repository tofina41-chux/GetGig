from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('profile/edit/', views.edit_profile, name='edit_profile'), # This is the "edit_profile" part
    path('notifications/', views.notifications_view, name='notifications'),
]