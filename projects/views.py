from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Application
from .forms import ProjectForm, ApplicationForm
from users.models import Notification # Import your Notification model
from django.contrib.admin.views.decorators import staff_member_required # If you want admin only
# Or just use login_required if any client can vet their own projects

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
        # Optional: messages.info(request, "You have already applied for this gig.")
        return redirect('projects:freelancer_dashboard')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.project = project
            application.freelancer = request.user
            application.save()

            # --- NEW NOTIFICATION LOGIC ---
            # Notify the client (the person who posted the project)
            Notification.objects.create(
                user=project.client, # The client
                message=f"New application from {request.user.username} for your project: '{project.title}'."
            )
            # ------------------------------

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


@login_required
def vet_application(request, application_id, status):
    application = get_object_or_404(Application, id=application_id)
    
    # Security: Only the project owner can vet applications
    # (Update '.client' below to match your Project model attribute)
    if application.project.client != request.user:
        messages.error(request, "You are not authorized to vet this application.")
        return redirect('projects:client_dashboard')

    if status in ['approved', 'rejected']:
        application.status = status
        application.save()
        
        # Notify the Freelancer
        Notification.objects.create(
            user=application.freelancer,
            message=f"Update: Your application for '{application.project.title}' has been {status}."
        )
        messages.success(request, f"Application {status} successfully.")
    
    return redirect('projects:client_dashboard')