from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import YamdbUser


@admin.register(YamdbUser)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('bio', 'role', 'confirmation_code')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('email', 'bio', 'role')}),
    )
