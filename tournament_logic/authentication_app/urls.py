from django.urls import path
from . import views 

urlpatterns = [
    # Remote auth
    path("", views.my_login, name="login"),
    path("home", views.home, name="home"),
    path("logout", views._logout, name="logout"),
    path("auth_intra", views.authorization_intra, name="auth_intra"),
    path("intra_authorize", views.intra_authorize, name="intra_authorize"),
]
