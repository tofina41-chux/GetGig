from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# 1. FOR NEW USERS (Sign Up)
class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'company_name', 'skills')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'w-full p-2 border rounded-lg focus:ring-2 focus:ring-[#0C6FBD] outline-none'})

# 2. FOR EXISTING USERS (Edit Profile Settings)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_image', 'bio', 'company_name', 'skills']
        
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field_name, field in self.fields.items():
        # Standard input styling
        if field_name != 'profile_image':
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-[#0C6FBD] focus:ring-4 focus:ring-blue-50 outline-none transition-all text-gray-700'
            })
        else:
            # File input styling
            field.widget.attrs.update({
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-bold file:bg-blue-50 file:text-[#0C6FBD] hover:file:bg-blue-100 transition-cursor'
            })
        # Logic: Hide fields based on user type so Joy doesn't see "Company Name"
        if self.instance and self.instance.user_type == 'freelancer':
            if 'company_name' in self.fields:
                del self.fields['company_name']
        elif self.instance and self.instance.user_type == 'client':
            if 'skills' in self.fields:
                del self.fields['skills']