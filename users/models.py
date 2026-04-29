from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.base import ContentFile
from PIL import Image
import os
from io import BytesIO

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='freelancer')
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default.png')
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    # Client specific
    company_name = models.CharField(max_length=100, blank=True)
    
    # Freelancer specific
    skills = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        # Only try to resize if there is an actual file to work with
        if self.profile_image:
            try:
                # This check handles the "No such file" issue during login/save
                # by ensuring the file exists before PIL tries to open it
                img = Image.open(self.profile_image)
                if img.height > 300 or img.width > 300:
                    output = BytesIO()
                    img.thumbnail((300, 300))
                    img_format = img.format if img.format else 'JPEG'
                    img.save(output, format=img_format, quality=85)
                    output.seek(0)
                    self.profile_image.save(
                        self.profile_image.name, 
                        ContentFile(output.read()), 
                        save=False
                    )
            except (Exception, FileNotFoundError) as e:
                print(f"Image resize skipped or failed: {e}")
                
        super().save(*args, **kwargs)