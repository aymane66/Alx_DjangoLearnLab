from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'date_of_birth', 'is_staff']
    ordering = ['email'] 

    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Info'), {'fields': ('date_of_birth', 'profile_photo')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional Info'), {'fields': ('date_of_birth', 'profile_photo')}),
    )

    search_fields = ['email']

