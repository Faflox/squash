from django.urls import path
from . import views

app_name = 'table'
urlpatterns = [
    path('', views.index, name='index'),
    path('add-player/', views.add_player, name='add_player'),
    path('start-tournament/', views.start_tournament, name='start_tournament'),
    path('reset-tournament/', views.reset_tournament, name='reset_tournament'),
    path('matches/', views.matches, name ='matches'),
    path('matches/score/<int:match_id>', views.match_score, name='match_score')
]
