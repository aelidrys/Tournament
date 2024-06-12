from authentication_app.views import user_profile, get_user
from channels.layers import get_channel_layer
from django.dispatch import receiver
from .models import tournament
from django.db import models
from .enums import Round, M_status
from django.shortcuts import render
from asgiref.sync import async_to_sync

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

def start_matche(request):
    user_prf = get_user(request)
    if user_prf is None:
        return
    matche_obj = user_prf.tournament.matches.all()
    context = {'matches':matche_obj, 'user_prf':user_prf}
    send_match_start(matche_obj, user_prf.tournament)
    return render(request, 'tournament/matches.html', context) 

def create_matches(request, tourn: tournament):
    players = tourn.players.all()
    p1 = None
    p2 = None
    i = 1
    for p in players:
        if i % 2 == 1:
            p1 = p
        else:
            p2 = p
            create_matche(p1, p2, tourn)
        i += 1
    start_matche(request)

def create_matche(p1, p2, trn):
    mtch = matche.objects.create(tourn=trn)
    mtch.player1 = p1
    mtch.player2 = p2
    mtch.round = trn.round
    mtch.status = M_status.UNPLAYED.value
    mtch.save()


def send_match_start(matche_obj: matche, user: user_profile):
    channel_layer = get_channel_layer()
    group_name = f'{user.tournament.name}_group'
    trn = tournament.objects.latest("id")

    print('views_group: ', group_name)
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "start_matche",
            "matche": matche_obj,
            "user": user,
        }    
    )
