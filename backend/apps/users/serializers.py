from rest_framework import serializers
from .models import TelegramUser, Favorite


class TelegramUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = TelegramUser
        fields = [
            "id",
            "telegram_id",
            "first_name",
            "last_name",
            "username",
            "phone",
            "language",
            "full_name",
            "created_at",
        ]
        read_only_fields = ["id", "telegram_id", "created_at"]


class FavoriteSerializer(serializers.ModelSerializer):
    from apps.products.serializers import ProductListSerializer

    product = ProductListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "product", "created_at"]
