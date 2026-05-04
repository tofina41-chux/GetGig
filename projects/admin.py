from django.contrib import admin
from .models import SiteConfiguration

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    # Prevent adding more than one configuration record
    def has_add_permission(self, request):
        if SiteConfiguration.objects.exists():
            return False
        return True