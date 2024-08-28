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
        cls.objects.update(points=0, games=0, qualified=False)
       
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
   
class FinalsMatch(models.Model):
    player1 = models.ForeignKey(Player, related_name='finals_player1',
                                on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='finals_player2',
                                on_delete=models.CASCADE)    
    level = models.CharField(max_length=50)    
    winner = models.ForeignKey(Player, default=None,
                               related_name='finals_match_winner',
                               on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.level}: {self.player1} vs {self.player2}"
    
    def update_winner(self):
        sets = self.sets.all()
        player1_sets_won = sets.filter(set_winner = self.player1).count()
        player2_sets_won = sets.filter(set_winner = self.player2).count()
        
        if player1_sets_won == 2:
            self.winner = self.player1
        elif player2_sets_won == 2:
            self.winner = self.player2
        else:
            self.winner = None
        self.save()
    
        
    
class Set(models.Model):
    match = models.ForeignKey(FinalsMatch, on_delete=models.CASCADE, 
                              related_name='sets')
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    set_num = models.IntegerField(default=0)
    set_winner = models.ForeignKey(Player, default=None, null=True, blank=True,
                                   related_name='set_winner',
                                   on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return (
            f"{self.match.level}: {self.match.player1} vs {self.match.player2}| " 
            f"SET: {self.set_num}, WYNIK: {self.score1} : {self.score2}")
        
    def determine_set_winner(self):
        if (self.score1 + self.score2) != 0:
            if self.score1 > self.score2:
                self.set_winner = self.match.player1
            elif self.score1 < self.score2:
                self.set_winner = self.match.player2 
    
    def save(self, *args, **kwargs):
        self.determine_set_winner()
        super().save(*args, **kwargs)
        self.match.update_winner()
        

class Placement(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    place = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f"{self.player} zajął {self.place}"      
    