from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import createPlayer, updateMatch, updateFinalsMatch, SetFormSet, modelformset_factory
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
    matches = Match.objects.order_by(-id)
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
        FinalsMatch.objects.all().delete()
        Player.reset_players()
        
        players = list(Player.objects.all())
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
        return redirect('table:index')
    return redirect('table:index')


def finals(request):
    semifinals = FinalsMatch.objects.filter(level='Półfinał')
    great_final = FinalsMatch.objects.filter(level='Finał')
    semi_winner_1 = None
    semi_winner_2 = None
    if semifinals.exists():
        semi_winner_1 = semifinals[0].winner
        semi_winner_2 = semifinals[1].winner
        if semifinals[1].winner and semifinals[0].winner and not great_final.exists():
            great_final = FinalsMatch.objects.create(player1=semi_winner_1,
                                                    player2=semi_winner_2,
                                                    level='Finał')
            for i in range(3):
                Set.objects.create(match=great_final,
                                set_num=(i+1))
    great_final = FinalsMatch.objects.filter(level='Finał').first()
    context={'semifinals': semifinals,
             'semi_winner_1': semi_winner_1,
             'semi_winner_2': semi_winner_2,
             'great_final': great_final}
    return render(request, 'table/finals.html', context)
        
@login_required     
def create_finals(request):
    FinalsMatch.objects.all().delete()
    top_players = Player.objects.order_by('-points', '-point_balance')[:4]
    Player.objects.filter(id__in=top_players).update(qualified=True)
    matchups = [
        (top_players[0], top_players[3]),
        (top_players[1], top_players[2])
    ]
    
    for player1, player2 in matchups:
        semi = FinalsMatch.objects.create(player1=player1, 
                                    player2=player2, 
                                    level='Półfinał')
        for i in range(3):
            Set.objects.create(match=semi,
                                set_num=(i+1))
    
    return redirect('table:finals')

@login_required
def change_finals_score(request, match_id):
    match = FinalsMatch.objects.get(id=match_id)
    sets = Set.objects.filter(match=match)
    formset = SetFormSet(queryset=sets)
    if request.method != 'POST':
        formset = SetFormSet(queryset=sets)
    else: 
        formset = SetFormSet(request.POST, queryset=sets)
        if formset.is_valid():
            formset.save()
            return redirect('table:finals')
        else:
            print(formset.errors)
            for form in formset:
                print(form.errors)
    return render(request, 'table/finals_match.html',
                  context={'match': match,'formset': formset})
