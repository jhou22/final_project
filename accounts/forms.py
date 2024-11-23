from django import forms
from .models import *
# from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
# from datetime import datetime

class CreatePlayerForm(SignupForm):
    dob = forms.DateField(label="Date of Birth", localize=True)
    class Meta:
        model = User
        
        fields = ['email', 'username', 'password1', 'password2', 'dob']
        
    def save(self, request):
        # print("SAVEING")
        # print(request.POST['dob'])
        #     # datetime.strptime(request.POST['dob'], '%Y-%m-%d')
        user = super(CreatePlayerForm, self).save(request)
        # email_address = request.POST['email']
        # username = request.POST['username']
        # dob = request.POST['dob']
        # PlayerProfile.objects.create(email=email_address, username=username, dob=dob, user=user)
        return user