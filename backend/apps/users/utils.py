from .models import TelegramUser


def get_users_count(request):
    """Return total users count for sidebar badge."""
    return TelegramUser.objects.filter(is_active=True).count()
