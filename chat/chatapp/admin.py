from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password")
