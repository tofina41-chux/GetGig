from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Application
from .forms import ProjectForm, ApplicationForm

@login_required
def client_dashboard(request):
    if request.user.user_type != 'client':
        return redirect('projects:freelancer_dashboard')
    # Get all projects created by this client
    my_projects = Project.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'clients/dashboard.html', {'projects': my_projects})

@login_required
def freelancer_dashboard(request):
    # 1. Security: If the user is actually a client, send them to their own dashboard
    if request.user.user_type == 'client':
        return redirect('projects:client_dashboard')
    
    # 2. Data: Get all projects created by ALL clients so the freelancer can browse them
    all_projects = Project.objects.all().order_by('-created_at')
    
    # 3. Delivery: Send that list to the FREELANCER-specific template
    return render(request, 'freelancers/dashboard.html', {'projects': all_projects})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.save()
            return redirect('projects:client_dashboard')
    else:
        form = ProjectForm()
    return render(request, 'clients/create_project.html', {'form': form})

@login_required
def apply_to_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Security: Don't let clients apply to jobs
    if request.user.user_type != 'freelancer':
        return redirect('projects:client_dashboard')

    # Optional: Check if already applied
    if Application.objects.filter(project=project, freelancer=request.user).exists():
        # You could add a django message here "Already applied!"
        return redirect('projects:freelancer_dashboard')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.project = project
            application.freelancer = request.user
            application.save()
            return redirect('projects:freelancer_dashboard')
    else:
        form = ApplicationForm()
    
    return render(request, 'freelancers/apply.html', {'form': form, 'project': project})



@login_required
def update_application_status(request, app_id, status):
    # Ensure only the client who owns the project can update the status
    application = get_object_or_404(Application, id=app_id, project__client=request.user)
    
    if status in ['accepted', 'rejected']:
        application.status = status
        application.save()
        
        if status == 'accepted':
            messages.success(request, f"Proposal from {application.freelancer.username} accepted!")
        else:
            messages.warning(request, f"Proposal from {application.freelancer.username} rejected.")
            
    return redirect('projects:client_dashboard')


@login_required
def freelancer_bids(request):
    if request.user.user_type != 'freelancer':
        return redirect('projects:client_dashboard')
    
    bids = Application.objects.filter(freelancer=request.user).select_related('project')
    return render(request, 'freelancers/my_bids.html', {'bids': bids})