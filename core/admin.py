from django.contrib import admin
from .models import *

# Register your models here.
class StoryModelAdmin(admin.ModelAdmin):
    model = Story
    list_display = ('user', 'id', 'create_on')
    list_filter = ['user']

class PostModelAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('user', 'id', 'caption', 'status', 'create_on')
    list_filter = ['user', 'status']

class LikeModelAdmin(admin.ModelAdmin):
    model = Like
    list_display = ('user', 'post', 'create_on')
    list_filter = ['user']

class CommentModelAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('user', 'post', 'create_on')
    list_filter = ['user']


admin.site.register(Story, StoryModelAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(Like, LikeModelAdmin)
admin.site.register(Comment, CommentModelAdmin)