from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password")


admin.site.register(Message)


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "reciever", "is_read")
