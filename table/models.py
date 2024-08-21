from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=50)
    points = models.SmallIntegerField()
    games = models.SmallIntegerField()
    qualified = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.name
       
class Match(models.Model):
    player1 = models.ForeignKey(Player, related_name='matches_as_player1',
                                on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='matches_as_player2',
                                on_delete=models.CASCADE)
    score1 = models.SmallIntegerField(default=0)
    score2 = models.SmallIntegerField(default=0)
    winner = models.ForeignKey(Player, default=None, related_name='winner_of_a_match', 
                               on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.player1} vs {self.player2}"
    
    #Zapewnia, że zwyciezca jest jeden z graczy
    def clean(self):  
        if self.winner and self.winner not in [self.player1, self.player2]:
            raise ValidationError('Zwycięzca musi być jednym z graczy')
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.player1.games += 1
        self.player2.games += 1
        self.player1.save()
        self.player2.save()
        
        super().save(*args, **kwargs)
    
class Placement(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    place = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f"{self.player} zajął {self.place}"