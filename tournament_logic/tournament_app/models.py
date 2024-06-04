from django.db import models
from .enums import Round, Tourn_status
from django.dispatch import receiver
from django.utils import timezone
# Create your models here.

class tournament(models.Model):
    name = models.CharField(default="four players", max_length=50)
    status = models.CharField(choices=Tourn_status.choices(), max_length=50,
        default=Tourn_status.PENDING.value)
    round = models.CharField(choices=Round.choices, default=Round.HALF.value,
        max_length=50)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
