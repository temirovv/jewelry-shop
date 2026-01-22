from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from apps.products.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    """Buyurtmalar API"""

    serializer_class = OrderSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        if hasattr(self.request.user, "telegram_id"):
            return Order.objects.filter(user=self.request.user).prefetch_related(
                "items__product"
            )
        return Order.objects.none()

    def create(self, request, *args, **kwargs):
        if not hasattr(request.user, "telegram_id"):
            return Response(
                {"error": "Avtorizatsiya talab qilinadi"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # Buyurtma yaratish
        order = Order.objects.create(
            user=request.user,
            phone=data["phone"],
            delivery_address=data.get("delivery_address", ""),
            comment=data.get("comment", ""),
        )

        # Elementlarni qo'shish
        for item_data in data["items"]:
            product = Product.objects.get(id=item_data["product_id"])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data["quantity"],
                price=product.price,
                size=item_data.get("size", ""),
            )

        order.calculate_total()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )
