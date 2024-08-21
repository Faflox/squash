from django.shortcuts import render, redirect, HttpResponse
from .forms import createPlayer, updateMatch
from .models import Player, Match
import random

# Create your views here.
def index(request):
    players = Player.objects.order_by('-points')
    context = {'players': players}
    return render(request, 'table/index.html', context)

def add_player(request):
    if request.method != 'POST':
        form = createPlayer()
    else:
        form = createPlayer(data=request.POST)
        if form.is_valid():
            new_player = form.save(commit=False)
            new_player.points = 0
            new_player.games = 0
            new_player.qualified = False
            new_player.save()
            return redirect('table:index')
    context = {'form': form}
    return render(request, 'table/add_player.html', context)


def matches(request):
    matches = Match.objects.order_by('winner')
    return render(request, 'table/matches.html', context={'matches': matches})

def match_score(request, match_id):
    match = Match.objects.get(id=match_id)
    if request.method != 'POST':
        form = updateMatch(instance=match)
    else:
        form = updateMatch(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return  redirect('table:matches')
    return render(request, 'table/match.html', context={'match': match,
                                                        'form': form})

def start_tournament(request):
    if request.method == 'POST':
        players = list(Player.objects.all())
        num_players = len(players)
        
        if num_players < 2:
            return HttpResponse("Not enough players to generate matches.")
        
        # Shuffle players
        random.shuffle(players)
        
        # Ensure each player plays exactly 4 matches
        matches = []
        num_matches = 3  # Each player should have exactly 4 matches

        # Create a dictionary to track the number of matches each player has
        player_match_counts = {player: 0 for player in players}
        
        # Generate matches
        for i in range(num_players):
            player1 = players[i]
            # Find opponents for player1
            for j in range(i + 1, num_players):
                player2 = players[j]
                
                if (player_match_counts[player1] < num_matches and
                    player_match_counts[player2] < num_matches):
                    
                    # Create a match
                    match = Match(player1=player1, player2=player2)
                    matches.append(match)
                    
                    # Update match counts
                    player_match_counts[player1] += 1
                    player_match_counts[player2] += 1
                    
                    # If each player has 4 matches, break the loop
                    if all(count >= num_matches for count in player_match_counts.values()):
                        break
            
            # Exit the outer loop if all players have 4 matches
            if all(count >= num_matches for count in player_match_counts.values()):
                break
        
        # Save all the matches to the database
        Match.objects.bulk_create(matches)
    
    return redirect('table:matches')

def reset_tournament(request):
    if request.method == "POST":
        Player.objects.all().delete()
        Match.objects.all().delete()
        return redirect('table:index')
    return redirect('table:index')