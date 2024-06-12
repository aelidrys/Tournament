from django.urls import path, include
from . import views, matches

urlpatterns = [
    path('', views.play_tournament, name='tournament'),
    path('matches', matches.start_matche, name='start_matche'),
]
