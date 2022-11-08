from email.policy import default
from re import A
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
CONTENT = [
    (0, "liked your post"),
    (1, "commented your post"),
    (2, "send you friend request"),
    (3, "added a new post"),
    (4, "added a new story")
]

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    content = models.IntegerField(choices=CONTENT)
    create_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-create_on']


class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
    
    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, partner):
        my_friend_list = self
        my_friend_list.remove_friend(partner)
        partner_friend_list = FriendList.objects.get(user=partner)
        partner_friend_list.remove_friend(self.user)
    
    def is_friend(self, account):
        if account in self.friends.all():
            return True
        return False

    @property
    def friend_count(self):
        return self.friends.count()


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    create_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_on']

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        receiver_friend_list.add_friend(self.sender)
        sender_friend_list = FriendList.objects.get(user=self.sender)
        sender_friend_list.add_friend(self.receiver)
        self.delete()

    def decline(self):
        self.delete()
    
    def cancer(self):
        self.delete()


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_to_user")
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to="chat", blank=True)
    create_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['create_on']
    
