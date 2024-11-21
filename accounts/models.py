from django.db import models
from django.contrib.auth.models import *
from django.urls import reverse
from django.utils import timezone
# Create your models here.

# in the event that User is extended to include more than just what the default User model provides
class User(AbstractUser):
    pass

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='user')
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    username = models.CharField(max_length=60, unique=True, verbose_name="username")
    join_date = models.DateTimeField(default=timezone.now, verbose_name='account creation date')
    dob = models.DateField(verbose_name='date of birth')
    profile_picture = models.ImageField(default='default-profile-icon.png', verbose_name='profile picture')
    fastest_guess = models.TimeField(verbose_name='time of fastest guess')
    bio = models.TextField(blank=False, verbose_name='bio')

    
    # def get_absolute_url(self):
    #     return reverse("profile", kwargs={"pk": self.pk})
    
    def __str__(self) -> str:
        return f'Player {self.username}, joined {self.dob}'
    
    
