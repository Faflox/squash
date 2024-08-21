from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=50)
    points = models.SmallIntegerField(default=0)
    games = models.SmallIntegerField(default=0)
    qualified = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.name
    
    @classmethod
    def reset_players(cls):
        cls.objects.update(points=0, games=0)
       
class Match(models.Model):
    player1 = models.ForeignKey(Player, related_name='matches_as_player1',
                                on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='matches_as_player2',
                                on_delete=models.CASCADE)
    score1 = models.SmallIntegerField(default=0)
    score2 = models.SmallIntegerField(default=0)
    winner = models.ForeignKey(Player, default=None, 
                               related_name='winner_of_a_match', 
                               on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.player1} {self.score1} vs {self.score2} {self.player2}"
    
    def clean(self):  
        #Zapewnia, że zwyciezca jest jeden z graczy
        if self.winner and self.winner not in [self.player1, self.player2]:
            raise ValidationError('Zwycięzca musi być jednym z graczy')
        
    def update_player_stats(self):
        players = [self.player1, self.player2]
        for player in players:
            player.games +=1
            if player == self.winner:
                player.points += 1
            player.save()
    
class Placement(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    place = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f"{self.player} zajął {self.place}"