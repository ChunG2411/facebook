import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from user.models import *
from interact.models import *
from core.models import *

class NotiConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = 'noti'
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
        text = data_json['text']

        user = data_json['user']
        user_obj = User.objects.get(username=user)
        
        match text:
            case "like":
                post_id = data_json['to_post_id']
                post_obj = Post.objects.get(id=post_id)

                noti = Notification.objects.filter(user=user_obj, to_user=post_obj.user, content=0, status=False)
                text = noti[0].get_content_display()

                async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                    {
                        'type'      : 'noti_like',
                        'user'      : noti[0].user.username,
                        'user_fullname' : noti[0].user.full_name,
                        'user_img'  : noti[0].user.avatar.url,
                        'to_user'   : noti[0].to_user.username,
                        'content'   : text,
                        'timestamp' : str(noti[0].create_on)[:19]
                    }
                )
            case "comment":
                post_id = data_json['to_post_id']
                post_obj = Post.objects.get(id=post_id)

                noti = Notification.objects.filter(user=user_obj, to_user=post_obj.user, content=1, status=False)
                text = noti[0].get_content_display()

                async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                    {
                        'type'      : 'noti_comment',
                        'user'      : noti[0].user.username,
                        'user_fullname' : noti[0].user.full_name,
                        'user_img'  : noti[0].user.avatar.url,
                        'to_user'   : noti[0].to_user.username,
                        'content'   : text,
                        'timestamp' : str(noti[0].create_on)[:19]
                    }
                )
            case "read_all":
                Notification.objects.filter(to_user=user_obj).update(status=True)
            
            case "add":
                to_user = data_json['to_user']
                to_user_obj = User.objects.get(username=to_user)
                noti = Notification.objects.filter(user=user_obj, to_user=to_user_obj, content=2)
                text = noti[0].get_content_display()
                
                async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                    {
                        'type'      : 'noti_friend',
                        'user'      : noti[0].user.username,
                        'user_fullname' : noti[0].user.full_name,
                        'user_img'  : noti[0].user.avatar.url,
                        'to_user'   : noti[0].to_user.username,
                        'content'   : text,
                        'timestamp' : str(noti[0].create_on)[:19]
                    }
                )

    
    def noti_like(self, e):
        self.send(text_data=json.dumps(e))
    
    def noti_comment(self, e):
        self.send(text_data=json.dumps(e))
    
    def noti_friend(self, e):
        self.send(text_data=json.dumps(e))


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = 'chat'
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
        text_data_json = json.loads(text_data)
        to_user = text_data_json['to_user']

        get_to_user = User.objects.get(username = to_user)
        Chat.objects.filter(user=get_to_user, to_user=self.user).update(status=True)
        
        try:
            text = text_data_json['text']
            Chat.objects.create(user=self.user, to_user=get_to_user, text=text, status=True)

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'message_text',
                    'user': self.user.username,
                    'user_fullname' : self.user.full_name,
                    'user_avatar' : self.user.avatar.url,
                    'to_user': to_user,
                    'text': text,
                }
            )
        except Exception:
            pass


    def message_text(self, event):
        self.send(text_data=json.dumps(event))

