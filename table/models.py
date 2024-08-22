from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=50)
    points = models.SmallIntegerField(default=0)
    games = models.SmallIntegerField(default=0)
    qualified = models.BooleanField(default=False)
    point_balance = models.IntegerField(default=0)
    
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
        #balans punktów
        self.player1.point_balance += (self.score1 - self.score2)
        self.player2.point_balance += (self.score2 - self.score1)
        #zwycięzca
        if self.score1 > self.score2:
            self.winner = self.player1
            self.player1.points += 1
        else:
            self.winner = self.player2
            self.player2.points += 1
        #zapis
        for player in players:
            player.games += 1
            player.save()
        self.save()
            
    
class Placement(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    place = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f"{self.player} zajął {self.place}"
    
    def create_placement(self):
        top_players = Player.objects.order_by('-points', '-point_balance')[:4]
                    
    