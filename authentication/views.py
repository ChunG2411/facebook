from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
User = get_user_model()

@csrf_exempt
def auth_login(request):
    template_name = 'authentication/login.html'
    
    if request.method == "POST":
        if "signup" in request.POST:
            signup_form = UserForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.success(request, 'Create fail')

        elif "login" in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is None:
                messages.success(request, 'Please check your username or password and try again')
                return render(request, template_name)
            else:   
                login(request, user)
                return redirect('home')

    else:
        signup_form = UserForm()
    context = {'signup_form':signup_form}
    return render(request, template_name, context)


def auth_logout(request):
    logout(request)
    return redirect('login')