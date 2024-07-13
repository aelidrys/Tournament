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
from .enums import Tourn_status

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
        user = self.scope.get("user", None)
        print('consumer {} receive'.format(user.username), flush=True)
        data = json.loads(text_data)
        if data['type'] == 'play_matche':
            trn = matche_simulation(user)
            refresh = 'true'
            if trn.status == Tourn_status.EN.value:
                refresh = 'false'
            self.send_matche_start(trn, refresh)

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
    
    def send_matche_start(self, trn: tournament, refresh):
        user = self.scope.get("user", None)
        print('send start_matche to user: {}'.format(user.username,
                    ), flush=True)
        matche_obj = get_matche(trn, user)
        m_res = 'win'
        if matche_obj is None:
            p1_img = None
            p1_name = None
            p2_img = None
            p2_name = None 
            m_res = 'lose'
        elif user.pk == matche_obj.player1.profile.user.pk:
            p1_img = matche_obj.player1.profile.image.url
            p1_name = matche_obj.player1.profile.user.username
            p2_img = matche_obj.player2.profile.image.url
            p2_name = matche_obj.player2.profile.user.username
        else:
            p1_img = matche_obj.player2.profile.image.url
            p1_name = matche_obj.player2.profile.user.username
            p2_img = matche_obj.player1.profile.image.url
            p2_name = matche_obj.player1.profile.user.username

        self.send(text_data=json.dumps({
            'type': 'matche',
            'm_res': m_res,
            'refresh': refresh,
            'matche': {
                'p1_image_url': p1_img,
                'p1_username': p1_name,
                'p2_image_url': p2_img,
                'p2_username': p2_name,
            },
        }))

        