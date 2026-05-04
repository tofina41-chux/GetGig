from django import forms
from .models import Project, Application

class ProjectForm(forms.ModelForm):
    # Place custom field definitions here
    requirements = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g. Above 18, Fluent in Python, English speaker...'}), 
        help_text="Enter requirements separated by commas"
    )
    class Meta:
        model = Project
        fields = ['title', 'description', 'budget', 'deadline', 'image', 'requirements']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'w-full p-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-ocean outline-none transition-all'})

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'bid_amount']