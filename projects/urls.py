from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('client/', views.client_dashboard, name='client_dashboard'),
    path('freelancer/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('create/', views.create_project, name='create_project'),
    path('apply/<int:project_id>/', views.apply_to_project, name='apply_to_project'),
    path('application/<int:app_id>/status/<str:status>/', views.update_application_status, name='update_status'),
    path('my-bids/', views.freelancer_bids, name='my_bids'),
]