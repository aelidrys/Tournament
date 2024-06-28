from django.shortcuts import render
from authentication_app.decorators import authenticated_only
from .models import tournament
from .matches import matche, create_matches
from authentication_app.views import get_user, user_profile
from .enums import Tourn_status, M_status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


@authenticated_only
def play_tournament(request):
    user_prf = get_user(request)
    if user_prf is None:
        return
    t_count = tournament.objects.count()
    if t_count == 0:
        trn = tournament.objects.create(name=f"trn{user_prf.user.id}")
    if user_prf.tournament is None:
        tourn_subscribing(request, user_prf)
        # trn = tournament.objects.latest("id")

    # print("after -> id: {}, name: {}, status: {}".format(trn.id, trn.name, trn.status))

    p_num = user_prf.tournament.players.count()
    players = {'players':user_prf.tournament.players.all(),
        'range': range(4-p_num), 'trn_name': user_prf.tournament.name}
    return render(request, 'tournament/tournament.html', players)


def tourn_subscribing(request, user_prf: user_profile):
    tourn = tournament.objects.latest("id")
    if tourn.status == Tourn_status.CLOSED.value:
        tourn_name = f"tourn_{user_prf.user.id}"
        new_tourn = tournament.objects.create(name=tourn_name)
        user_prf.tournament = new_tourn
        user_prf.save()
    else:
        user_prf.tournament = tourn
        user_prf.save()
        t_players = user_prf.tournament.players.count()
        if t_players == 4:
            tourn.status = Tourn_status.CLOSED.value
            tourn.save()
            create_matches(request, tourn)
        else:
            send_tournament_update(tourn)



def send_tournament_update(trn: tournament):
    channel_layer = get_channel_layer()
    room_group_name = f'{trn.name}_group'
    trn = tournament.objects.latest("id")
    players = trn.players.all()
    rang = list(range(4-trn.players.count()))
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'update_tournament',
            'tourn_players': [
                {'image_url': player.image.url, 'username': player.user.username}
                for player in players
            ],
            'range': rang,
        }
    )
    print('tourn_up send to group: ', room_group_name)