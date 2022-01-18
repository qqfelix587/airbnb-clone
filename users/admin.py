from django.contrib import admin
from . import models


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    """Custom User Admin"""

    list_display = ("username", "email", "gender", "language", "currency", "superhost")
    # admin panel 에 노출할 field
    list_filter = ("language", "currency", "superhost")
    # admin panel의 filter기능
