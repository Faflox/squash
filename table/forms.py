from django import forms
from .models import Player, Match

class createPlayer(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']
        labels = {'name': 'Nazwa Gracza'}