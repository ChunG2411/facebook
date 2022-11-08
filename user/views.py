from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import get_user_model

from core.models import *
from interact.models import *
from user.forms import UserEditForm
from interact.views import recent_search

# Create your views here.
User = get_user_model()

class Profile(View):
    template_name_auth = 'user/authenticated_profile.html'
    template_name_anon = 'user/anonymous_profile.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = User.objects.get(username=username)
        edit_form = UserEditForm(instance=request.user)

        liked = []
        commented = []
        all_post = Post.objects.filter(user=user)
        all_like = Like.objects.filter(user=request.user)
        all_comment = Comment.objects.filter(user=request.user)
        all_noti = Notification.objects.filter(to_user=request.user)
        all_noti_not_read = Notification.objects.filter(to_user=request.user, status=False)
        all_user = User.objects.all()

        all_chat = []
        chat = Chat.objects.all()
        for i in chat:
            if i.user == request.user or i.to_user == request.user:
                all_chat.append(i)

        all_chat_navbar = []
        for i in all_chat:
            if i.user not in all_chat_navbar:
                all_chat_navbar.append(i.user)
            if i.to_user not in all_chat_navbar:
                all_chat_navbar.append(i.to_user)
        
        chat_receive_not_read = Chat.objects.filter(to_user=request.user, status=False)
        all_chat_not_read = []
        if chat_receive_not_read:
            for i in chat_receive_not_read:
                if i.user not in all_chat_not_read:
                    all_chat_not_read.append(i.user)
                if i.to_user not in all_chat_not_read:
                    all_chat_not_read.append(i.to_user)

        try:
            all_friend = FriendList.objects.get(user=user)
        except Exception as e:
            FriendList.objects.create(user=user)
            all_friend = FriendList.objects.get(user=user)

        try:
            all_my_friends = FriendList.objects.get(user=request.user)
        except Exception as e:
            FriendList.objects.create(user=request.user)
            all_my_friends = FriendList.objects.get(user=request.user)

        try:
            send_friend_request = FriendRequest.objects.filter(sender=request.user, receiver=user)
        except Exception as e:
            send_friend_request = None
        try:
            receive_friend_request = FriendRequest.objects.filter(sender=user, receiver=request.user)
        except Exception as e:
            receive_friend_request = None

        if user != request.user:
            if all_friend.is_friend(request.user):
                is_friend = True
            else:
                is_friend = False
            if send_friend_request:
                sended = True  
            else:
                sended = False
            if receive_friend_request:
                receive = True
            else:
                receive = False

        search_term = request.GET.get('query')
        if search_term:
            recent_search.append(search_term)
        if len(recent_search) < 5:
            recent_display = recent_search
        else:
            recent_display = recent_search[len(recent_search)-5:len(recent_search)]

        for i in range(len(all_like)):
            if len(liked) <= len(all_like):
                liked.append(0)
                liked[i] = all_like[i].post.id
        
        for i in range(len(all_comment)):
            if len(commented) <= len(all_comment):
                commented.append(0)
                commented[i] = all_comment[i].post.id

        if request.user.username == username:
            context = {'user':user, 'edit_form': edit_form,
                        'all_post': all_post, 'liked': liked, 'commented': commented,
                        'all_noti': all_noti, 'all_noti_not_read': all_noti_not_read,
                        'recent_display': recent_display,
                        'all_friend': all_friend, 'all_chat': all_chat, 'all_user': all_user,
                        'all_chat_navbar': all_chat_navbar, 'all_chat_not_read': all_chat_not_read,}
            return render(request, self.template_name_auth, context)
        else:
            context = {'user':user,
                        'all_post': all_post, 'liked': liked, 'commented': commented,
                        'all_noti': all_noti, 'all_noti_not_read': all_noti_not_read,
                        'recent_display': recent_display,
                        'all_friend': all_my_friends, 'all_anon_friend': all_friend, 'is_friend': is_friend, 'sended': sended, 'receive': receive,
                        'all_chat': all_chat, 'all_user': all_user,
                        'all_chat_navbar': all_chat_navbar, 'all_chat_not_read': all_chat_not_read,}
            return render(request, self.template_name_anon, context)


class DeletePost(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        Post.objects.get(id=post_id).delete()
        return redirect(request.META.get('HTTP_REFERER'))


class EditProfile(View):
    template_name_auth = 'user/authenticated_profile.html'

    def post(self, request, *args, **kwargs):
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            context = {'edit_form': form}
            return render(request, self.template_name_auth, context)
