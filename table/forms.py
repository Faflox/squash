from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Player, Match

class createPlayer(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']
        labels = {'name': 'Nazwa Gracza'}
        
class updateMatch(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['score1', 'score2', 'winner']
        
    def __init__(self, *args, **kwargs):
        match = kwargs.get('instance')
        super(updateMatch, self).__init__(*args, **kwargs)
        if match:
            self.fields['winner'].queryset = Player.objects.filter(id__in=[
                match.player1.id, match.player2.id
            ])