from authentication_app.models import user_profile
from .models import tournament
from django.db import models
from .enums import Round, M_status
from django.dispatch import receiver

class matche(models.Model):
    tourn = models.ForeignKey(tournament, on_delete=models.CASCADE,
        related_name="matches")
    round = models.CharField(max_length=50, default=Round.HALF.value,
        choices=Round.choices())
    player1 = models.OneToOneField(user_profile, related_name="p1",
        on_delete=models.CASCADE, null=True)
    player2 = models.OneToOneField(user_profile, related_name="p2",
        on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50, default=M_status.UNPLAYED.value,
        choices=M_status.choices())


