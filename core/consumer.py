import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from core.models import *
from interact.models import *
from user.models import *

class UserInteractConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = 'interact'
        self.user = None
        self.user_status = None

    def connect(self):
        self.user = self.scope['user']
        try:
            self.user_status = UserStatus.objects.get(name="user_online")
        except Exception:
            UserStatus.objects.create(name="user_online")
            self.user_status = UserStatus.objects.get(name="user_online")

        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.user_status.online.add(self.user)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type' : 'list_user_online',
                'list' : [user.username for user in self.user_status.online.all()]
            }
        )
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        self.user_status.online.remove(self.user)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type' : 'list_user_online',
                'list' : [user.username for user in self.user_status.online.all()]
            }
        )
    
    def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        context = data_json['active']

        user = data_json['user']
        post_id = data_json['post_id']

        user_obj = User.objects.get(username=user)
        post_obj = Post.objects.get(id=post_id)

        match context:
            case "like":
                Like.objects.create(user=user_obj, post=post_obj)
                Notification.objects.create(user=user_obj, to_user=post_obj.user, content=0)

                async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                    {
                        'type'      : 'like_post',
                        'post_id'   : post_id
                    }
                )

            case "unlike":
                Like.objects.filter(user=user_obj, post=post_obj).delete()
                try:
                    Notification.objects.filter(user=user_obj, to_user=post_obj.user, content=0)[0].delete()
                except Exception:
                    pass
                async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                    {
                        'type'      : 'unlike_post',
                        'post_id'   : post_id
                    }
                )

            case "comment":
                content = data_json['text']
                cmt = Comment.objects.create(user=user_obj, post=post_obj, text=content)
                Notification.objects.create(user=user_obj, to_user=post_obj.user, content=1)

                async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                    {
                        'type'      : 'comment_post',
                        'user'      : cmt.user.username,
                        'full_name' : cmt.user.full_name,
                        'user_img'  : cmt.user.avatar.url,
                        'post_id'   : post_id,
                        'text'      : content,
                        'cmt_id'    : cmt.id
                    }
                )
            
            case "remove_comment":
                cmt_id = data_json['cmt_id']
                Comment.objects.get(id=cmt_id).delete()
                try:
                    Notification.objects.filter(user=user_obj, to_user=post_obj.user, content=1)[0].delete()
                except Exception:
                    pass    
                
                async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                    {
                        'type'     : 'rmv_cmt',
                        'cmt_id'   : cmt_id,
                        'post_id'   : post_id
                    }
                )


    def list_user_online(self, e):
        self.send(text_data=json.dumps(e))
    
    def like_post(self, e):
        self.send(text_data=json.dumps(e))
        
    def unlike_post(self, e):
        self.send(text_data=json.dumps(e))
    
    def noti(self, e):
        self.send(text_data=json.dumps(e))
    
    def comment_post(self, e):
        self.send(text_data=json.dumps(e))
    
    def rmv_cmt(self, e):
        self.send(text_data=json.dumps(e))