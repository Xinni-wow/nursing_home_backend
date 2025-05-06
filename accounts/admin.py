from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'user_type', 'full_name', 'phone', 'address', 'email', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'full_name', 'phone', 'address')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'full_name', 'phone', 'address')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
