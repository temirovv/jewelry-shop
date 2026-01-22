from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TelegramUserSerializer


@api_view(["GET"])
def get_current_user(request):
    """Joriy foydalanuvchi ma'lumotlari"""
    if not request.user or not hasattr(request.user, "telegram_id"):
        return Response(
            {"error": "Foydalanuvchi topilmadi"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    serializer = TelegramUserSerializer(request.user)
    return Response(serializer.data)


@api_view(["PATCH"])
def update_current_user(request):
    """Foydalanuvchi ma'lumotlarini yangilash"""
    if not request.user or not hasattr(request.user, "telegram_id"):
        return Response(
            {"error": "Foydalanuvchi topilmadi"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    serializer = TelegramUserSerializer(
        request.user, data=request.data, partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
