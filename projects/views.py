from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

# Import your models and forms
from .models import Project, Application, SiteConfiguration
from .forms import ProjectForm, ApplicationForm
from users.models import Notification 

# This fixes the CustomUser Manager error
User = get_user_model()

# --- PUBLIC VIEWS ---

def landing_page(request):
    """The main entry point for the site."""
    config = SiteConfiguration.objects.first() 
    
    stats = {
        'total_gigs': Project.objects.filter(status='active').count(),
        'total_freelancers': User.objects.filter(user_type='freelancer').count(), 
        'total_payouts': "12.5k",
    }
    
    return render(request, 'landing.html', {
        'config': config,
        'stats': stats
    })

# --- DASHBOARD VIEWS ---

@login_required
def client_dashboard(request):
    if request.user.user_type != 'client':
        return redirect('projects:freelancer_dashboard')
    my_projects = Project.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'clients/dashboard.html', {'projects': my_projects})

@login_required
def freelancer_dashboard(request):
    if request.user.user_type == 'client':
        return redirect('projects:client_dashboard')
    all_projects = Project.objects.order_by('-created_at')
    return render(request, 'freelancers/dashboard.html', {'projects': all_projects})

# --- PROJECT MANAGEMENT ---

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            raw_reqs = form.cleaned_data.get('requirements', '')
            project.requirements = [r.strip() for r in raw_reqs.split(',') if r.strip()]
            project.save()
            messages.success(request, "Project posted!")
            return redirect('projects:client_dashboard')
    else:
        form = ProjectForm()
    return render(request, 'clients/create_project.html', {'form': form})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, client=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            raw_reqs = form.cleaned_data.get('requirements', '')
            project.requirements = [r.strip() for r in raw_reqs.split(',') if r.strip()]
            project.applications.exclude(status='archived').update(status='archived')
            form.save()
            return redirect('projects:client_dashboard')
    else:
        initial_reqs = ", ".join(project.requirements)
        form = ProjectForm(instance=project, initial={'requirements': initial_reqs})
    return render(request, 'clients/create_project.html', {'form': form, 'editing': True})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, client=request.user)
    project.delete()
    return redirect('projects:client_dashboard')

@login_required
def toggle_project_status(request, project_id):
    project = get_object_or_404(Project, id=project_id, client=request.user)
    
    if project.status == 'active':
        project.status = 'closed'
    else:
        project.status = 'active'
        # Feature: Archive past applications so freelancers can re-apply for this new phase!
        project.applications.filter(status__in=['pending', 'accepted', 'rejected']).update(status='archived')
        
    project.save()
    return redirect('projects:client_dashboard')

# --- APPLICATION & VETTING ---

@login_required
def apply_to_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.user_type != 'freelancer':
        return redirect('projects:client_dashboard')

    # Change: Check for existing applications but ignore old archived rounds
    has_active_application = Application.objects.filter(
        project=project, 
        freelancer=request.user
    ).exclude(status='archived').exists()

    if has_active_application:
        messages.info(request, "Already applied to the current active round.")
        return redirect('projects:freelancer_dashboard')

    if not project.can_apply:
        messages.error(request, "This gig is no longer accepting applications.")
        return redirect('projects:freelancer_dashboard')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.project = project
            application.freelancer = request.user
            application.met_requirements = request.POST.getlist('met_requirements')
            application.save()
            
            Notification.objects.create(
                user=project.client,
                message=f"New application for '{project.title}'."
            )
            messages.success(request, "Application submitted successfully!")
            return redirect('projects:freelancer_dashboard')
    else:
        form = ApplicationForm()
        
    return render(request, 'freelancers/apply.html', {'form': form, 'project': project})

@login_required
def vet_application(request, application_id=None, app_id=None, status=None):
    """
    Handles both URL variants: 'vet_application' and 'update_application_status'
    """
    # Use whichever ID the URL provided
    target_id = application_id or app_id
    application = get_object_or_404(Application, id=target_id)
    
    if application.project.client != request.user:
        messages.error(request, "Unauthorized.")
        return redirect('projects:client_dashboard')

    if status in ['accepted', 'rejected', 'approved']:
        application.status = status
        application.save()
        Notification.objects.create(
            user=application.freelancer,
            message=f"Application for '{application.project.title}' was {status}."
        )
        messages.success(request, f"Application {status}!")
    
    return redirect('projects:client_dashboard')

# ALIAS: This makes sure the 'update_application_status' name exists for urls.py
update_application_status = vet_application

@login_required
def freelancer_bids(request):
    bids = Application.objects.filter(freelancer=request.user).select_related('project')
    return render(request, 'freelancers/my_bids.html', {'bids': bids})