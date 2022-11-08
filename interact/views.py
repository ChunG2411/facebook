from django.shortcuts import redirect, render
from django.views import View

from .models import *
from core.models import *
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()
recent_search =[]

class Search(View):
    template_name = 'core/search.html'
    
    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('query')

        search_result_user = []
        search_result_post = []
        user = User.objects.all()
        post = Post.objects.filter(status=1)    

        liked = []
        commented = []
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
            all_friend = FriendList.objects.get(user=request.user)
        except Exception as e:
            FriendList.objects.create(user=request.user)
            all_friend = FriendList.objects.get(user=request.user)

        if search_term:
            recent_search.append(search_term)
        if len(recent_search) < 5:
            recent_display = recent_search
        else:
            recent_display = recent_search[len(recent_search)-5:len(recent_search)]

        if search_term:
            for i in user:
                if search_term in i.full_name:
                    search_result_user.append(i)
            for i in post:
                if search_term in i.caption:
                    search_result_post.append(i)
        else:
            search_result_user = User.objects.none()
            search_result_post = Post.objects.none()

        for i in range(len(all_like)):
            if len(liked) <= len(all_like):
                liked.append(0)
                liked[i] = all_like[i].post.id
        
        for i in range(len(all_comment)):
            if len(commented) <= len(all_comment):
                commented.append(0)
                commented[i] = all_comment[i].post.id
        
        context = {'search_result_user': search_result_user, 'search_result_post': search_result_post, 'recent_display': recent_display,
                    'liked': liked, 'commented': commented,
                    'all_noti': all_noti, 'all_noti_not_read': all_noti_not_read,
                    'all_chat': all_chat, 'all_chat_navbar': all_chat_navbar, 'all_chat_not_read': all_chat_not_read,
                    'all_friend': all_friend, 'all_user': all_user}
        return render(request, self.template_name, context)

