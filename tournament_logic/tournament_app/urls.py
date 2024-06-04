from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.play_tournament, name='tournament'),
    path('matches', views.matches, name='matches'),
]
