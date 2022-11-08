from django.urls import path, include
from .views import *

urlpatterns = [
    path('', auth_login, name="login"),
    path('logout', auth_logout, name="logout"),
]