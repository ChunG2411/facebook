from django.contrib import admin
from .models import *

# Register your models here.
class NotificationModelAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ['user', 'to_user', 'content', 'status', 'create_on']
    list_filter = ['user', 'to_user', 'content', 'status']

class FriendListModelAdmin(admin.ModelAdmin):
    model = FriendList
    list_display = ['user', 'friend_count']
    list_filter = ['user']

class FriendRequestModelAdmin(admin.ModelAdmin):
    model = FriendRequest
    list_display = ['sender', 'receiver', 'create_on']
    list_filter = ['sender', 'receiver']

class ChatModelAdmin(admin.ModelAdmin):
    model = Chat
    list_display = ['user', 'to_user', 'id', 'status','create_on']
    list_filter = ['user', 'to_user']


admin.site.register(Notification, NotificationModelAdmin)
admin.site.register(FriendList, FriendListModelAdmin)
admin.site.register(FriendRequest, FriendRequestModelAdmin)
admin.site.register(Chat, ChatModelAdmin)