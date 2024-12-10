from django import forms
from .models import *
class GameForm(forms.Form):
    guess = forms.DecimalField(label="Guess", decimal_places=2, max_digits=100)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message', 'image']