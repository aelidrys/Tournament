from django.shortcuts import render
from authentication_app.decorators import authenticated_only
from .models import tournament
from .matches import start_matche
from authentication_app.views import get_user
from .enums import U_status
from .tournament import tourn_subscribing


@authenticated_only
def play_tournament(request):
    user_prf = get_user(request)
    if user_prf is None:
        return
    t_count = tournament.objects.count()
    if t_count == 0:
        trn = tournament.objects.create(name=f"trn{user_prf.user.id}")
    if  user_prf.status != U_status.IG.value:
        m = tourn_subscribing(request, user_prf)
        trn = tournament.objects.latest('id')
        if m == 1:
            return start_matche(request, trn)

    trn = tournament.objects.latest('id')
    p_num = trn.trn_players.count()
    players = {'players':trn.trn_players.all(),
        'range': range(4-p_num), 'trn_name': trn.name}
    return render(request, 'tournament/tournament.html', players)


