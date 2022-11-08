from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from authentication.forms import *

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = UserForm
    model = User
    list_display = ('full_name','username', 'email', 'gender','is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        ('Personal details', {'fields' : ('email', 'full_name', 'username','gender', 'avatar', 'background')}),
        ('Optional', {'fields' : ('phone_number', 'home_town', 'biography')}),
        ('Permission', {'fields' : ('is_staff', 'is_active', 'is_superuser')})
    )
    add_fieldsets = (
        ('Personal details', {'fields' : ('email', 'full_name', 'username', 'gender', 'avatar', 'background', 'password1', 'password2')}),
        ('Optionals', {'fields' : ('phone_number', 'home_town', 'biography')}),
        ('Permissions', {'fields' : ('is_staff', 'is_active')})
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserStatus)