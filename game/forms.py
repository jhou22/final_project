from django import forms

class GameForm(forms.Form):
    guess = forms.DecimalField(label="Guess", decimal_places=2, max_digits=100)