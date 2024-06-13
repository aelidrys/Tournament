from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from random import randint
from time import sleep
from .views import play_tournament
from asgiref.sync import async_to_sync
from .models import tournament

class WSConsumer(WebsocketConsumer):
    def connect(self):
        trn = tournament.objects.latest("id")
        self.room_group_name = f'{trn.name}_group'
        
        print('con_group: ',self.room_group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()

    def receive(self, text_data):
        print('receive')
        pass

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    def update_tournament(self, event):
        print('send_tournament_update called!!!')
        players = event['tourn_players']
        rang = event['range']
        
        # Send updated player data to WebSocket
        self.send(text_data=json.dumps({
            'type': 'tourn',
            'tourn_players': players,
            'range': rang,
        }))

    def start_matche(self, event):
        matche_obj = event['matche']
        user = event['user']

        self.send(text_data=json.dumps({
            'type': 'matche',
            'matche': matche_obj,
            'user': user,
        }))

        