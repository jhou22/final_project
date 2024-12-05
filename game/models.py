from django.db import models
from accounts.models import *

# Create your models here.
class Item(models.Model):
    price = models.DecimalField(verbose_name='Item price', default='0.00', decimal_places=2, max_digits=10, blank=False, null=False)
    name = models.TextField(verbose_name='Item name', default='Kroger item', blank=False, null=False)
    image = models.ImageField(verbose_name='Item image', upload_to='item-images/', default='defaults/grocery-item.jpg', blank=False, null=False)

    def __str__(self) -> str:
        return f'{self.name}'

class CommonPuzzle(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, verbose_name='Puzzle item', blank=False, null=False)
    
    class Meta:
        abstract = True

class DailyPuzzle(CommonPuzzle):
    date = models.DateField(verbose_name='Date of daily puzzle', auto_now_add=True, blank=False, null=False)
    
class PracticePuzzle(CommonPuzzle):
    pass

class Guess(models.Model):
    owner = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, verbose_name='Owner of guess', blank=False, null=False)
    
    daily_puzzle = models.ForeignKey(DailyPuzzle, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Daily Puzzle')
    practice_puzzle = models.ForeignKey(PracticePuzzle, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Practice Puzzle')
    
    guess_one = models.DecimalField(verbose_name='Guess 1', max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    guess_two = models.DecimalField(verbose_name='Guess 2', max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    guess_three = models.DecimalField(verbose_name='Guess 3', max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    guess_four = models.DecimalField(verbose_name='Guess 4', max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    guess_five = models.DecimalField(verbose_name='Guess 5', max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    guess_six = models.DecimalField(verbose_name='Guess 6', max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    
class Comment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Time of comment written", blank=False, null=False)
    user = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, null=False, blank=False)
    image = models.ImageField(blank=True, null=True, verbose_name='Comment image')
    puzzle = models.ForeignKey(DailyPuzzle, null=False, blank=False, on_delete=models.CASCADE, verbose_name='Puzzle where comment is written')
    message = models.TextField(blank=False, null=False, default='')
    
    def __str__(self) -> str:
        return f'{self.user}\'s comment at {self.timestamp}'
    
    