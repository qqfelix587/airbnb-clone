from django.contrib import admin
from django.utils.html import mark_safe
from django.contrib.auth.admin import UserAdmin
from rooms import models as room_models
from . import models


class RoomInline(admin.StackedInline):
    model = room_models.Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        'get_thumbnail',
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
        
    )

    def get_thumbnail(self, obj):
        if (obj.avatar):
            return mark_safe(f'<img width=50px  src="{obj.avatar.url}"')

    get_thumbnail.short_description = "Thumbnail"
