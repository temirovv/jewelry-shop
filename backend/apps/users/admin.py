from django.contrib import admin
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ["telegram_id", "first_name", "last_name", "username", "phone", "is_active", "created_at"]
    list_filter = ["is_active", "language", "created_at"]
    search_fields = ["first_name", "last_name", "username", "phone", "telegram_id"]
    readonly_fields = ["telegram_id", "created_at", "updated_at"]
    ordering = ["-created_at"]
