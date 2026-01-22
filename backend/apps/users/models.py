from django.db import models


class TelegramUser(models.Model):
    """Telegram orqali kirgan foydalanuvchi"""

    LANGUAGE_CHOICES = [
        ("uz", "O'zbekcha"),
        ("ru", "Русский"),
    ]

    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    username = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="uz")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Telegram foydalanuvchi"
        verbose_name_plural = "Telegram foydalanuvchilar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} ({self.telegram_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
