from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import get_user_model

from .forms import *
from interact.models import *
from interact.views import recent_search


# Create your views here.
User = get_user_model()

class HomeView(View):
    template_name = 'core/main.html'

    def get(self, request, *args, **kwargs):
        form = PostForm()

        liked = []
        commented = []
        user = request.user

        all_story = Story.objects.filter(create_on__gte=datetime.now()-timedelta(days=1))
        all_post = Post.objects.filter(status=1)
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

        context = {'user':user, 'form': form,
                    'all_story': all_story, 'all_post': all_post, 'liked': liked, 'commented': commented,
                    'all_noti': all_noti, 'all_noti_not_read': all_noti_not_read,
                    'recent_display': recent_display, 'all_chat_navbar' :all_chat_navbar, 'all_chat_not_read': all_chat_not_read,
                    'all_friend': all_friend, 'all_chat': all_chat, 'all_user': all_user}
        return render(request, self.template_name, context)


class PostCreate(View):
    template_name = 'core/main.html'

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post(
                user = request.user,
                caption = request.POST.get('caption'),
                image = request.FILES.get('image'),
                status = request.POST['status']
            )
            post.save()
            return redirect(request.META.get('HTTP_REFERER')) 
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


class FriendView(View):
    template_name = 'core/friend.html'

    def get(self, request):
        all_friend = FriendList.objects.get(user=request.user)
        receive_friend_request = FriendRequest.objects.filter(receiver=request.user)
        send_friend_request = FriendRequest.objects.filter(sender=request.user)

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

        context = { 'all_friend': all_friend, 'all_user': all_user, 'all_chat': all_chat,
                    'receive_friend_request': receive_friend_request,
                    'send_friend_request': send_friend_request,
                    'all_chat_navbar': all_chat_navbar,  'all_chat_not_read': all_chat_not_read,
                }
        return render(request, self.template_name, context)


class StoryView(View):
    template_name = 'core/story.html'

    def get(self, request, *args, **kwargs):
        form = StoryForm()

        all_story = Story.objects.filter(create_on__gte=datetime.now()-timedelta(days=1))
        all_noti = Notification.objects.filter(to_user=request.user)
        all_user = User.objects.all()

        try:
            all_friend = FriendList.objects.get(user=request.user)
        except Exception as e:
            FriendList.objects.create(user=request.user)
            all_friend = FriendList.objects.get(user=request.user)

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

        context = {'all_story': all_story, 'form': form,
                    'all_noti': all_noti, 'all_chat': all_chat, 'all_friend': all_friend, 'all_user': all_user,
                    'all_chat_navbar': all_chat_navbar, 'all_chat_not_read': all_chat_not_read,}
        return render(request, self.template_name, context)
    
    
class StoryCreate(View):
    template_name = 'core/story.html'

    def post(self, request, *args, **kwargs):
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = Story(
                    user = request.user,
                    image = request.FILES.get('image')
            )
            story.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


class DeleteStory(View):
    def post(self, request, *args, **kwargs):
        story_id = kwargs.get('id')
        Story.objects.get(id=story_id).delete()
        return redirect(request.META.get('HTTP_REFERER'))