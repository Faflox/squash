from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import createPlayer, updateMatch
from .models import Player, Match, FinalsMatch, Set

# Create your views here.
def index(request):
    players = Player.objects.order_by('-points', '-point_balance')
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
    matches = Match.objects.all()
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
        schedule = generate_schedule(players)
        for player1, player2 in schedule:
            Match.objects.create(player1=player1, player2=player2)
    return redirect('table:matches')

def generate_schedule(players):
    if len(players) == 8:
        matches = [
            (players[0], players[1]), (players[2], players[3]), 
            (players[4], players[5]), (players[6], players[7]),
            (players[0], players[2]), (players[1], players[3]), 
            (players[4], players[6]), (players[5], players[7]),
            (players[0], players[3]), (players[1], players[2]), 
            (players[4], players[7]), (players[5], players[6])
        ]
    elif len(players) == 9:
        matches = [
            (players[0], players[1]), (players[0], players[2]), 
            (players[0], players[3]),
            (players[1], players[4]), (players[1], players[5]),
            (players[2], players[6]), (players[2], players[7]),
            (players[3], players[8]),
            (players[4], players[6]), (players[4], players[7]),
            (players[5], players[8]), (players[5], players[3]),
            (players[6], players[0]), (players[6], players[8]),
            (players[7], players[1]), (players[7], players[3]),
            (players[8], players[2]), (players[8], players[4])
        ]
    return matches

@login_required
def reset_tournament(request):
    if request.method == "POST":
        Player.objects.all().delete()
        Match.objects.all().delete()
        return redirect('table:index')
    return redirect('table:index')


def finals(request):
    finals = FinalsMatch.objects.all()
    return render(request, 'table/finals.html', context={'finals': finals})
        
@login_required     
def create_finals(request):
    FinalsMatch.objects.all().delete()
    Set.objects.all().delete()
    top_players = Player.objects.order_by('-points', '-point_balance')[:4]
    matchups = [
        (top_players[0], top_players[3]),
        (top_players[1], top_players[2])
    ]
    
    for player1, player2 in matchups:
        FinalsMatch.objects.create(player1=player1, 
                                    player2=player2, 
                                    level='Półfinał')
    
    semis = FinalsMatch.objects.all()
    for semi in semis:
        for set in range(3):
            Set.objects.create(match=semi,
                               set_num=(set+1))
    
    return redirect('table:finals')

def change_finals_score(request, match_id):
    return render(request, 'table/finals_match.html')