from django.http import HttpResponse
from django.shortcuts import redirect
from .models import user_profile

def unauthentication_user(view_fun):
    def wrapper_fun(request, *args, **kwargs):
        user_prf = get_user(request)
        if user_prf:
            return redirect('home')
        return view_fun(request, *args, **kwargs)
    return wrapper_fun

def authenticated_only(view_fun):
    def wrapper_fun(request, *arg, **args):
        user_prf = get_user(request)
        if user_prf:
            request.user = user_prf.user
            return view_fun(request, *arg, **args)
        return redirect('login')
    return wrapper_fun

def get_user(request):
    if request.user.is_authenticated:
        try:
            user_prf = user_profile.objects.get(user=request.user)
            return user_prf
        except:
            return None
    try:
        access_token = request.session['access_token']
    except:
        return None
    user = None
    if access_token:
        try:
            user = user_profile.objects.get(access_token=access_token)
        except:
            return None
    return user
