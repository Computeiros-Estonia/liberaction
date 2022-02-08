from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from liberaction.users.models import User

class CustomUserAdmin(UserAdmin):
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
