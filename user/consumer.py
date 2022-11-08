import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from core.models import *
from interact.models import *
from user.models import User

class FriendConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = 'friend'
        self.user = None
    
    def connect(self):
        self.user = self.scope['user']
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
    
    def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        user = data_json['user']
        active = data_json['active']

        user_obj = User.objects.get(username=user)
        match active:
            case "remove":
                friend_list = FriendList.objects.get(user=self.user)
                friend_list.unfriend(user_obj)
            case "add":
                FriendRequest.objects.create(sender=self.user, receiver=user_obj)
                Notification.objects.create(user=self.user, to_user=user_obj, content=2)
            case "cancer":
                try:
                    FriendRequest.objects.get(sender=self.user, receiver=user_obj).cancer()
                    Notification.objects.get(user=self.user, to_user=user_obj, content=2).delete()
                except Exception:
                    pass
            case "confirm":
                try:
                    FriendRequest.objects.get(sender=user_obj, receiver=self.user).accept()
                    Notification.objects.get(user=user_obj, to_user=self.user, content=2).delete()
                except Exception:
                    pass
            case "decline":
                try:
                    FriendRequest.objects.get(sender=user_obj, receiver=self.user).decline()
                    Notification.objects.get(user=user_obj, to_user=self.user, content=2).delete()
                except Exception:
                    pass
    