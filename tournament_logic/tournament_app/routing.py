from django.urls import path
from .consumers import WSConsumer

ws_urlpatterns = [
    path('ws/tourn/', WSConsumer.as_asgi()),
]