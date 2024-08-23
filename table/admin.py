from django.contrib import admin
from .models import Player, Match, Placement, FinalsMatch, Set

# Register your models here.
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Placement)
admin.site.register(FinalsMatch)
admin.site.register(Set)