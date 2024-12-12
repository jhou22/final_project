# Signals for Django-Allauth

from datetime import datetime
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import PlayerProfile

# creates account when email verified
@receiver(user_signed_up)
def email_confirmed(request, user, **kwargs):
    email_address = request.POST['email']
    username = request.POST['username']
    dob = convert_to_datetime(request.POST['dob'])
    # dob_datetime = convert_to_datetime(dob)
    PlayerProfile.objects.create(email=email_address, username=username, dob=dob, user=user)
    
    # converts datetime based on string
def convert_to_datetime(date_string):
    common_formats = [
        "%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", 
        "%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M:%S", "%d-%m-%Y %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%fZ",
        "%B %d, %Y", "%d %B, %Y"
    ]

    for fmt in common_formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            pass

    raise ValueError("Could not auto-detect date format for string: {}".format(date_string))
