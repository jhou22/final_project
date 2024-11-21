from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class CreatePlayerForm(UserCreationForm):
    dob = forms.DateField(label="Date of Birth")
    class Meta:
        model = User
        
        fields = ['email', 'username', 'password1', 'password2', 'dob']