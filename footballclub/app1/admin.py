from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'age', 'role', 'jno', 'cdate', 'sal', 'img')
    list_filter = ('role',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

admin.site.register(CustomUser, CustomUserAdmin)
