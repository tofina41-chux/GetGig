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
    path('application/<int:application_id>/vet/<str:status>/', views.vet_application, name='vet_application'),
    path('project/<int:project_id>/toggle/', views.toggle_project_status, name='toggle_project_status'),
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('project/<int:project_id>/edit/', views.edit_project, name='edit_project'),
]