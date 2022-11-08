from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<str:username>', Profile.as_view(), name="profile"),
    path('post/delete/<str:id>', DeletePost.as_view(), name="delete_post"),
    path('profile/<str:username>/edit/', EditProfile.as_view(), name="edit_profile"),
]