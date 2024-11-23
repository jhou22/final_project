from django.db import models
from accounts.models import *

# Create your models here.
class Item(models.Model):
    price = models.DecimalField(verbose_name='Item price', default='0.00', decimal_places=2, max_digits=10)
    name = models.TextField(blank=False, verbose_name='Item name', default='')
    image = models.ImageField(null=True, verbose_name='Item image', upload_to='item-images/')
    
    def __str__(self) -> str:
        return f'{self.name}'
    
class Comment(models.Model):
    timestamp = models.DateTimeField(auto_now=True, verbose_name="Time of comment written")
    user = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, verbose_name='Comment image')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Item where comment is written')
    message = models.TextField(blank=False)
    
    def __str__(self) -> str:
        return f'{self.user}\'s comment at {self.timestamp}'
    
    