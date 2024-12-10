from datetime import date
from django.db import models
from django.contrib.auth.models import *
from django.urls import reverse
from django.utils import timezone
import uuid
# Create your models here.

# in the event that User is extended to include more than just what the default User model provides
class User(AbstractUser):
    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})

class PlayerProfile(models.Model):
    # with one-to-one fields and foreign keys, playerprofile and user can access each other due to the reverse relationships (related_name field)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='user')
    email = models.EmailField(verbose_name="Email address", max_length=255, unique=True)
    username = models.CharField(max_length=60, unique=True, verbose_name="Username", default=uuid.uuid4())
    join_date = models.DateTimeField(default=timezone.now, verbose_name='Account creation date')
    dob = models.DateField(verbose_name='date of birth', default=date(1970, 1, 1).isoformat())
    profile_picture = models.ImageField(default='default-profile-icon.png', verbose_name='Profile picture', upload_to='profile-pictures/')
    bio = models.TextField(blank=False, verbose_name='Bio', default='No information written')

    
    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})
    
    def __str__(self) -> str:
        return f'{self.username}'
    
    def add_friend(self, to_user):
        if self == to_user:
            return # adding yourself lol
        if self is None:
            return # do you not exist or something
        if to_user is None:
            return # adding no one? impossible
        if len(list(Friend.objects.filter(from_user=self, to_user=to_user))) != 0:
            return
        if len(list(Friend.objects.filter(from_user=to_user, to_user=self))) != 0:
            return
        Friend.objects.create(from_user=self, to_user=to_user)

    def is_friends(self, to_user):
        return len(list(Friend.objects.filter(from_user=self, to_user=to_user))) != 0 or len(list(Friend.objects.filter(from_user=to_user, to_user=self))) != 0
    
    def friends_since(self, to_user):
        if len(list(Friend.objects.filter(from_user=self, to_user=to_user))) != 0:
            return Friend.objects.filter(from_user=self, to_user=to_user)[0].friendship_created
        elif len(list(Friend.objects.filter(from_user=to_user, to_user=self))) != 0:
            return Friend.objects.filter(from_user=to_user, to_user=self)[0].friendship_created
        else:
            return None
class Friend(models.Model):
    from_user = models.ForeignKey(PlayerProfile, verbose_name='From user', on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(PlayerProfile, verbose_name='To user', on_delete=models.CASCADE, related_name='to_user')
    friendship_created = models.DateTimeField(verbose_name='Time of friendship creation', default=timezone.now)
    
    def __str__(self) -> str:
        return f'{self.from_user} and {self.to_user}'
