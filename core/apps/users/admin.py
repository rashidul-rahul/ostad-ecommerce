from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.apps.users.models import User


class CustomUserAdmin(UserAdmin):
    search_fields = ("username", "email", "phone_number")
    list_filter = UserAdmin.list_filter
    list_display = ("phone_no", "username", "email", "first_name", "last_name",)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, CustomUserAdmin)
