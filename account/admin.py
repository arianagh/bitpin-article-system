from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(User, CustomUserAdmin)
