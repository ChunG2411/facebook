from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import *

# Create your models here.

GENDER = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('N', 'Prefer not to say')
]

class User(AbstractUser):
    full_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER)

    avatar = models.ImageField(upload_to='avatar_img', null=True, blank=True, default='avatar_img/user.png')
    background = models.ImageField(upload_to='background_img', null=True, blank=True, default='background_img/background.jpg')
    home_town = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    biography = models.TextField(max_length=255, null=True, blank=True)

    first_name = None
    last_name = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'username',]

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name

    @property
    def post_count(self):
        return self.post_set.count()


class UserStatus(models.Model):
    name = models.CharField(max_length = 20)
    online = models.ManyToManyField(to=User, blank=True)

    def online_count(self):
        return self.online.count()

    def __str__(self):
        return f"{self.name}: {self.online_count()} online"