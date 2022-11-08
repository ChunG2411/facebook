from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'username', 'password1', 'password2', 'gender']
