from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from random import randint
from time import sleep
# local import
from .views import play_tournament
from .models import tournament
from .matches import get_matche, matche_simulation

class WSConsumer(WebsocketConsumer):
    def connect(self):
        trn = tournament.objects.latest("id")
        self.room_group_name = f'{trn.name}_group'
        
        user = self.scope.get("user", None)
        # if user:
        #     print('user_name: ', user.username)
        # else:
        #     print("no user")
        print("user {} added to group: {}".format(user.username,
            self.room_group_name), flush=True)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()

    def receive(self, text_data):
        print('receive', flush=True)
        user = self.scope.get("user", None)
        data = json.loads(text_data)
        if data['type'] == 'play_matche':
            trn = matche_simulation(user)
            self.send_matche_start(trn, 'false')

    def disconnect(self, close_code):
        print("DISCONNECT", flush=True)
        user = self.scope.get("user", None)
        print("user {} rmoved from group: {}".format(user.username,
            self.room_group_name), flush=True)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def update_tournament(self, event):
        print('send_tournament_update called!!!')
        players = event['tourn_players']
        rang = event['range']

        # Send updated player data to WebSocket
        user = self.scope.get("user", None)
        if user:
            print('username: ', user.username)
        else:
            print("no user")
        self.send(text_data=json.dumps({
            'type': 'tourn',
            'tourn_players': players,
            'range': rang,
        }))

    def start_matche(self, event):
        trn_id = event['trn_id']
        refresh = event['refresh']
        trn = tournament.objects.get(id=trn_id)
        self.send_matche_start(trn, refresh)
    
    def send_matche_start(self, trn, refresh):
        user = self.scope.get("user", None)
        matche_obj = get_matche(trn.matches.all(), user)
        if user.pk == matche_obj.player1.profile.user.pk:
            plyr1 = matche_obj.player1
            plyr2 = matche_obj.player2
        else:
            plyr1 = matche_obj.player2
            plyr2 = matche_obj.player1

        print('start_matche by user: {}'.format(user.username,
                    ), flush=True)
        self.send(text_data=json.dumps({
            'type': 'matche',
            'refresh': refresh,
            'matche': {
                'p1_image_url': plyr1.profile.image.url,
                'p1_username': plyr1.profile.user.username,
                'p2_image_url': plyr2.profile.image.url,
                'p2_username': plyr2.profile.user.username,
            },
        }))

        