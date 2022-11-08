from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
STATUS = [
    (0, "Only me"),
    (1, "Publish")
]

class Story(models.Model):
    image = models.ImageField(upload_to='story')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_on']


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(max_length=255)
    image = models.ImageField(upload_to='post', blank=True)
    status = models.IntegerField(choices=STATUS, default=1)
    create_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_on']

    @property
    def like_count(self):
        return self.like_set.count()
    
    @property
    def comment_count(self):
        return self.comment_set.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    create_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_on']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    create_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_on']
