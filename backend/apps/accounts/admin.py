from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "display_name", "email", "rating_estimate", "is_staff")
    search_fields = ("username", "display_name", "email")
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Chess trainer",
            {
                "fields": (
                    "display_name",
                    "rating_estimate",
                    "board_orientation_hint",
                    "google_sub",
                )
            },
        ),
    )
