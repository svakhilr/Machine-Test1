from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = ( "username","email", "is_staff")
    ordering = ("id",)

    fieldsets = (
        (None, {"fields": ( "password",)}),
        (_("Personal info"), {"fields": ("username","email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

