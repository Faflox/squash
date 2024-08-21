from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import createPlayer, updateMatch
from .models import Player, Match
import random

# Create your views here.
def index(request):
    players = Player.objects.order_by('-points')
    return render(request, 'table/index.html', context={'players': players})

@login_required
def add_player(request):
    if request.method != 'POST':
        form = createPlayer()
    else:
        form = createPlayer(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('table:index')
    return render(request, 'table/add_player.html', context={'form': form})

def matches(request):
    matches = Match.objects.order_by('winner')
    return render(request, 'table/matches.html', context={'matches': matches})

@login_required
def match_score(request, match_id):
    match = Match.objects.get(id=match_id)
    if request.method != 'POST':
        form = updateMatch(instance=match)
    else:
        form = updateMatch(request.POST, instance=match)
        if form.is_valid():
            form.save()
            match.update_player_stats()
            return  redirect('table:matches')
    return render(request, 'table/match.html', context={'match': match,
                                                        'form': form})

@login_required
def start_tournament(request):
    if request.method == 'POST':
        Match.objects.all().delete()
        Player.reset_players()
        
        players = list(Player.objects.all())
        num_players = len(players)
        random.shuffle(players)
        matches = []
        
        #ilość meczy zmieniaj tutaj--------------------------------------------
        num_matches = 3
        player_match_counts = {player: 0 for player in players}
        
        for i in range(num_players):
            player1 = players[i]
            for j in range(i + 1, num_players):
                player2 = players[j]
                
                if (player_match_counts[player1] < num_matches and
                    player_match_counts[player2] < num_matches):
                    
                    match = Match(player1=player1, player2=player2)
                    matches.append(match)
                    

                    player_match_counts[player1] += 1
                    player_match_counts[player2] += 1
                    
                    if all(count >= num_matches for count in player_match_counts.values()):
                        break
            
            if all(count >= num_matches for count in player_match_counts.values()):
                break
        
        random.shuffle(matches)
        Match.objects.bulk_create(matches)
    
    return redirect('table:matches')

@login_required
def reset_tournament(request):
    if request.method == "POST":
        Player.objects.all().delete()
        Match.objects.all().delete()
        return redirect('table:index')
    return redirect('table:index')