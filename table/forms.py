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
        fields = ['score1', 'score2']