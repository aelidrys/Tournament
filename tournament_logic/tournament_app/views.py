from django.shortcuts import render
from authentication_app.decorators import autenticated_only
from .models import tournament
from .matches import matche
from authentication_app.views import get_user, user_profile
from .enums import Tourn_status, M_status


@autenticated_only
def play_tournament(request):
    user_prf = get_user(request)
    if user_prf is None:
        return
    t_count = tournament.objects.count()
    if t_count == 0:
        trn = tournament.objects.create(name=f"trn{user_prf.user.id}")
    if user_prf.tournament is None:
        tourn_subscribing(user_prf)
        trn = tournament.objects.latest("id")
        print("after -> id: {}, name: {}, status: {}".format(trn.id, trn.name, trn.status))


    p_num = user_prf.tournament.players.count()
    players = {'players':user_prf.tournament.players.all(),
        'range': range(4-p_num), 'trn_name': user_prf.tournament.name}
    return render(request, 'tournament/tournament.html', players)


def tourn_subscribing(user_prf: user_profile):
    tourn = tournament.objects.latest("id")
    if tourn.status == Tourn_status.CLOSED.value:
        tourn_name = f"tourn_{user_prf.user.id}"
        print("new_trn_name: ", tourn_name)
        new_tourn = tournament.objects.create(name=tourn_name)
        user_prf.tournament = new_tourn
        user_prf.save()
    else:
        user_prf.tournament = tourn
        user_prf.save()
        t_players = user_prf.tournament.players.count()
        print('t_player', t_players)
        if t_players == 4:
            tourn.status = Tourn_status.CLOSED.value
            tourn.save()
            create_matches(tourn)

def create_matches(tourn: tournament):
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


def create_matche(p1, p2, trn):
    mtch = matche.objects.create(tourn=trn)
    mtch.player1 = p1
    mtch.player2 = p2
    mtch.round = trn.round
    mtch.status = M_status.UNPLAYED.value
    mtch.save()

def matches(request):
    user_prf = get_user(request)
    if user_prf is None:
        return
    matches = user_prf.tournament.matches.all()
    context = {'matches':matches, 'user_prf':user_prf}
    return render(request, 'tournament/matches.html', context) 
