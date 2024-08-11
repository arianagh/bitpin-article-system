from django.contrib import admin

from account.models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'created_at', 'updated_at')


admin.site.register(User, CustomUserAdmin)
