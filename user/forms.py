from .models import *
from django import forms

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'avatar', 'background', 'email', 'gender', 'biography', 'home_town', 'phone_number']

