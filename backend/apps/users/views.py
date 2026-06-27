from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import viewsets

from apps.products.models import Product

from .models import Favorite
from .serializers import TelegramUserSerializer, FavoriteSerializer


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


class FavoriteViewSet(viewsets.ModelViewSet):
    """Sevimlilar ro'yxati, qo'shish, olib tashlash."""

    serializer_class = FavoriteSerializer
    http_method_names = ["get", "post", "delete"]
    pagination_class = None

    def get_queryset(self):
        if not hasattr(self.request.user, "telegram_id"):
            return Favorite.objects.none()
        return (
            Favorite.objects.filter(user=self.request.user)
            .select_related("product", "product__category")
            .prefetch_related("product__images")
        )

    @action(detail=False, methods=["post"], url_path="toggle")
    def toggle(self, request):
        """product_id'ni qabul qiladi; mavjud bo'lsa o'chiradi, aks holda qo'shadi."""
        if not hasattr(request.user, "telegram_id"):
            return Response(
                {"error": "Avtorizatsiya talab qilinadi"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        product_id = request.data.get("product_id")
        if not product_id:
            return Response(
                {"error": "product_id majburiy"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not Product.objects.filter(id=product_id, is_active=True).exists():
            return Response(
                {"error": "Mahsulot topilmadi"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fav = Favorite.objects.filter(user=request.user, product_id=product_id).first()
        if fav:
            fav.delete()
            return Response({"is_favorite": False, "product_id": int(product_id)})

        Favorite.objects.create(user=request.user, product_id=product_id)
        return Response(
            {"is_favorite": True, "product_id": int(product_id)},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["delete"], url_path="clear")
    def clear(self, request):
        """Barcha sevimlilarni o'chirish."""
        if not hasattr(request.user, "telegram_id"):
            return Response(
                {"error": "Avtorizatsiya talab qilinadi"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        deleted, _ = Favorite.objects.filter(user=request.user).delete()
        return Response({"deleted": deleted})
