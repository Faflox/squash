from django.contrib import admin
from .models import Player, Match, Placement

# Register your models here.
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Placement)