from django.db import models
from django.conf import settings
from django.utils import timezone
from cloudinary.models import CloudinaryField  # Imported native cloud field pipeline

class Project(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Swapped to CloudinaryField to bypass Vercel read-only disk error
    image = CloudinaryField('image', folder='project_images', blank=True, null=True)
    
    requirements = models.JSONField(default=list, blank=True) # Stores ['Above 18', 'Fluent Spanish']
    status = models.CharField(
        max_length=20, 
        choices=[('active', 'Active'), ('ended', 'Ended')], 
        default='active'
    )

    @property
    def is_ended(self):
        return self.status == 'ended' or self.deadline < timezone.localdate()

    @property
    def days_until_deadline(self):
        return (self.deadline - timezone.localdate()).days

    @property
    def status_label(self):
        if self.is_ended:
            return 'Ended'
        if self.deadline == timezone.localdate():
            return 'Happening Today'
        if self.days_until_deadline == 1:
            return 'Due tomorrow'
        return f"Due in {self.days_until_deadline} days"

    @property
    def can_apply(self):
        return self.status == 'active' and self.deadline >= timezone.localdate()

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') # New Field
    created_at = models.DateTimeField(auto_now_add=True)
    met_requirements = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.freelancer.username} - {self.project.title}"


class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default="GetGig")
    hero_title = models.CharField(
        max_length=255,
        default="A better way to hire and work with elite freelance talent."
    )
    hero_subtitle = models.TextField(
        default="Post premium gigs, match with qualified freelancers, and manage proposals all in one social freelancing marketplace."
    )
    
    # Swapped to CloudinaryField to clear your admin area save crashes
    hero_image = CloudinaryField('image', folder='site_assets', blank=True, null=True)

    class Meta:
        verbose_name = "Site Configuration"

    def __str__(self):
        return self.site_name