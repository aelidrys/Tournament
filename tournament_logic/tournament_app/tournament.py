from .models import tournament
from .matches import create_matches, player, send_match_start
from authentication_app.views import profile
from .enums import Tourn_status, U_status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def tourn_subscribing(request, user_prf: profile):
    tourn = tournament.objects.latest("id")
    if tourn.status == Tourn_status.ST.value:
        tourn_name = f"tourn_{user_prf.user.id}"
        new_tourn = tournament.objects.create(name=tourn_name)
        plyr = player.objects.create(tournament=new_tourn, profile=user_prf)
        plyr.name = f'player_{user_prf.user.username}'
        plyr.save()
        # user_prf.status = U_status.IG.value
        user_prf.save()
    else:
        plyr = player.objects.create(tournament=tourn, profile=user_prf)
        plyr.name = f'player_{user_prf.user.username}'
        plyr.save()
        # user_prf.status = U_status.IG.value
        user_prf.save()
        t_players = plyr.tournament.trn_players.count()
        if t_players == 4:
            tourn.status = Tourn_status.ST.value
            tourn.save()
            create_matches(tourn)
            send_match_start(tourn, 'true')
            return 1
        else:
            send_tournament_update(tourn)
    return 0



def send_tournament_update(tourn: tournament):
    channel_layer = get_channel_layer()
    room_group_name = f'{tourn.name}_group'
    players = tourn.trn_players.all()
    rang = list(range(4-tourn.trn_players.count()))
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'update_tournament',
            'start_status': tourn.status,
            'tourn_players': [
                {'image_url': player.profile.image.url, 'username': player.profile.user.username}
                for player in players
            ],
            'range': rang,
        }
    )
    print('tourn_up send to group: ', room_group_name)

