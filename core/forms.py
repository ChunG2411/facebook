from .models import *
from django import forms

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image', 'status']