from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
)
from apps.products.models import Product


def get_or_create_cart(user):
    """Foydalanuvchi savatini olish yoki yaratish"""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@api_view(["GET"])
def get_cart(request):
    """Savatni ko'rish"""
    if not hasattr(request.user, "telegram_id"):
        return Response({"error": "Avtorizatsiya talab qilinadi"}, status=401)

    cart = get_or_create_cart(request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(["POST"])
def add_to_cart(request):
    """Savatga qo'shish"""
    if not hasattr(request.user, "telegram_id"):
        return Response({"error": "Avtorizatsiya talab qilinadi"}, status=401)

    serializer = AddToCartSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    try:
        product = Product.objects.get(id=data["product_id"], is_active=True)
    except Product.DoesNotExist:
        return Response({"error": "Mahsulot topilmadi"}, status=404)

    if not product.in_stock:
        return Response({"error": "Mahsulot sotuvda yo'q"}, status=400)

    cart = get_or_create_cart(request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=data.get("size", ""),
        defaults={"quantity": data["quantity"]},
    )

    if not created:
        cart_item.quantity += data["quantity"]
        cart_item.save()

    return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
def update_cart_item(request, item_id):
    """Savat elementini yangilash"""
    if not hasattr(request.user, "telegram_id"):
        return Response({"error": "Avtorizatsiya talab qilinadi"}, status=401)

    try:
        cart_item = CartItem.objects.get(
            id=item_id, cart__user=request.user
        )
    except CartItem.DoesNotExist:
        return Response({"error": "Element topilmadi"}, status=404)

    serializer = UpdateCartItemSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    quantity = serializer.validated_data["quantity"]

    if quantity == 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    cart = get_or_create_cart(request.user)
    return Response(CartSerializer(cart).data)


@api_view(["DELETE"])
def remove_from_cart(request, item_id):
    """Savatdan o'chirish"""
    if not hasattr(request.user, "telegram_id"):
        return Response({"error": "Avtorizatsiya talab qilinadi"}, status=401)

    try:
        cart_item = CartItem.objects.get(
            id=item_id, cart__user=request.user
        )
        cart_item.delete()
    except CartItem.DoesNotExist:
        return Response({"error": "Element topilmadi"}, status=404)

    cart = get_or_create_cart(request.user)
    return Response(CartSerializer(cart).data)


@api_view(["DELETE"])
def clear_cart(request):
    """Savatni tozalash"""
    if not hasattr(request.user, "telegram_id"):
        return Response({"error": "Avtorizatsiya talab qilinadi"}, status=401)

    cart = get_or_create_cart(request.user)
    cart.items.all().delete()

    return Response(CartSerializer(cart).data)
