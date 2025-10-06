from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('phone_number',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)