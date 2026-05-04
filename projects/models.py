from django.db import models
from django.conf import settings

class Project(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    requirements = models.JSONField(default=list, blank=True) # Stores ['Above 18', 'Fluent Spanish']
    status = models.CharField(
        max_length=20, 
        choices=[('active', 'Active'), ('ended', 'Ended')], 
        default='active'
    )

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
    hero_title = models.CharField(max_length=255, default="Find the perfect talent for your next big idea.")
    hero_subtitle = models.TextField(default="A premium marketplace for high-end freelancers.")
    hero_image = models.ImageField(upload_to='site_assets/', blank=True, null=True)

    class Meta:
        verbose_name = "Site Configuration"

    def __str__(self):
        return self.site_name