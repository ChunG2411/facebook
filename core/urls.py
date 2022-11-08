from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('home/', login_required(HomeView.as_view()), name="home"),
    path('story/', login_required(StoryView.as_view()), name="story"),
    path('friend/', login_required(FriendView.as_view()), name="friend"),
    
    path('post/create/', login_required(PostCreate.as_view()), name="post_create"),
    path('story/create/', login_required(StoryCreate.as_view()), name="story_create"),

    path('story/delete/<int:id>', login_required(DeleteStory.as_view()), name="delete_story"),
]