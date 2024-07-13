from authentication_app.views import profile, get_user
from channels.layers import get_channel_layer
from django.dispatch import receiver
from .models import tournament
from django.db import models
from .enums import Round, M_status, Tourn_status
from django.shortcuts import render
from asgiref.sync import async_to_sync
from django.utils import timezone
from django.http import JsonResponse




class player(models.Model):
    name = models.CharField(max_length=100, default='player_x')
    tournament = models.ForeignKey(tournament, on_delete=models.CASCADE,
        related_name="trn_players")
    profile = models.ForeignKey(profile, related_name="players",
        on_delete=models.CASCADE, null=True)
    won = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class matche(models.Model):
    tourn = models.ForeignKey(tournament, on_delete=models.CASCADE,
        related_name="matches")
    round = models.CharField(max_length=50, default=Round.HF.value,
        choices=Round.choices())
    player1 = models.ForeignKey(player, related_name="matche_p1",
        on_delete=models.CASCADE, null=True)
    player2 = models.ForeignKey(player, related_name="matche_p2",
        on_delete=models.CASCADE, null=True)
    winner = models.ForeignKey(player, related_name="m_win",
        on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50, default=M_status.UNP.value,
        choices=M_status.choices())


def start_matche(request, tourn):
    user_prf = get_user(request)
    if user_prf is None:
        return
    matches = tourn.matches.all()

    context = {'matches':matches, 'user_prf':user_prf}
    return render(request, 'tournament/matche.html', context) 

def create_matches(tourn: tournament):
    print('create_matches', flush=True)
    players = tourn.trn_players.all()
    won_players = [plyr for plyr in players if plyr.won] 
    if len(won_players) == 1:
        # send_match_start(tourn, 'false')
        tourn.status = Tourn_status.EN.value
        tourn.save()
        return
    p1 = None
    p2 = None
    i = 1
    for p in won_players:
        if i % 2 == 1:
            p1 = p
        else:
            p2 = p
            create_matche(p1, p2, tourn)
        i += 1
    # send_match_start(tourn, 'true')


def create_matche(p1, p2, trn):
    mtch = matche.objects.create(tourn=trn)
    mtch.player1 = p1
    mtch.player2 = p2
    mtch.round = trn.round
    mtch.status = M_status.UNP.value
    mtch.save()


def send_match_start(trn: tournament, refresh):
    channel_layer = get_channel_layer()
    group_name = f'{trn.name}_group'

    print('send_match_start to : ', group_name, flush=True)
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "start_matche",
            'refresh': refresh,
            "trn_id": trn.pk,
        }
    )


def matche_simulation(user):
    trn = tournament.objects.latest('id')
    print('matche simulation Round: ', trn.round, flush=True)
    matches = trn.matches.all()
    i = 1
    for matche in matches:
        if i % 2:
            matche.player2.won = False
            matche.player2.save()
            matche.winner = matche.player1
            matche.status = M_status.PLY.value
            matche.save()
        else:
            matche.player1.won = False
            matche.player1.save()
            matche.winner = matche.player2
            matche.status = M_status.PLY.value
            matche.save()
        i += 1
    return new_round(trn)


def update_round(trn : tournament):
    if trn.round == Round.QU.value:
        trn.round = Round.HF.value
        trn.save()
    if trn.round == Round.HF.value:
        trn.round = Round.FN.value
        trn.save()



def new_round(trn):

    update_round(trn)
    create_matches(trn)
    matches = matche.objects.filter(status=M_status.UNP.value)
    for m in matches:
        print('plyer1_name', m.player1.profile.user.username, flush=True)
    return trn


def get_matche(trn, user):
    mtches = matche.objects.filter(round=trn.round)
    for mtche in mtches:
        if mtche.player1.profile.user == user:
            return mtche
        if mtche.player2.profile.user == user:
            return mtche
    print('no mtche exist', flush=True)
    return None

def get_player(user_prf):
    players = user_prf.players.all()
    plyr_count = players.count()
    i = 0
    for plyr in players:
        # print('plyr_trn_name ', plyr.tournament.name, flush=True)
        player = plyr
        i += 1
        if i == plyr_count:
            return player