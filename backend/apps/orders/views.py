import logging
from decimal import Decimal
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from .utils import send_order_notification
from apps.products.models import Product

logger = logging.getLogger(__name__)

FREE_DELIVERY_THRESHOLD = Decimal("500000")
DELIVERY_FEE = Decimal("30000")


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

        try:
            with transaction.atomic():
                # BTS region/city
                delivery_region = None
                delivery_city = None
                if data.get("delivery_region_id"):
                    from apps.delivery.models import BTSRegion, BTSCity

                    delivery_region = BTSRegion.objects.filter(
                        bts_id=data["delivery_region_id"]
                    ).first()
                    if data.get("delivery_city_id"):
                        delivery_city = BTSCity.objects.filter(
                            bts_id=data["delivery_city_id"]
                        ).first()

                # Buyurtma yaratish
                order = Order.objects.create(
                    user=request.user,
                    phone=data["phone"],
                    delivery_address=data.get("delivery_address", ""),
                    comment=data.get("comment", ""),
                    payment_method=data.get("payment_method", "cash"),
                    delivery_region=delivery_region,
                    delivery_city=delivery_city,
                )

                # Elementlarni qo'shish
                items_total = Decimal("0")
                for item_data in data["items"]:
                    product = Product.objects.select_for_update().get(
                        id=item_data["product_id"]
                    )

                    if not product.in_stock:
                        raise ValueError(f"'{product.name}' sotuvda yo'q")

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item_data["quantity"],
                        price=product.price,
                        size=item_data.get("size", ""),
                    )
                    items_total += product.price * item_data["quantity"]

                # Yetkazish narxini hisoblash
                delivery_fee = Decimal("0")
                if delivery_region and delivery_city:
                    # BTS orqali hisoblash
                    try:
                        from apps.delivery.services import calculate_delivery_cost

                        bts_result = calculate_delivery_cost(
                            delivery_region.bts_id, delivery_city.bts_id
                        )
                        bts_fee = bts_result.get("delivery_fee")
                        if bts_fee:
                            delivery_fee = Decimal(str(bts_fee))
                    except Exception as e:
                        logger.warning(f"BTS delivery fee hisoblashda xatolik: {e}")
                        # Fallback: hardcoded fee
                        if items_total < FREE_DELIVERY_THRESHOLD:
                            delivery_fee = DELIVERY_FEE
                else:
                    # BTS tanlanmagan — hardcoded logic
                    if items_total < FREE_DELIVERY_THRESHOLD:
                        delivery_fee = DELIVERY_FEE

                order.delivery_fee = delivery_fee
                order.total = items_total + delivery_fee
                order.save(update_fields=["delivery_fee", "total"])

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Buyurtmadan keyin foydalanuvchi savatini tozalash
        try:
            cart = request.user.cart
            cart.items.all().delete()
        except Exception:
            pass

        # Admin userlarga notification yuborish
        try:
            send_order_notification(order)
        except Exception as e:
            logger.error(f"Notification yuborishda xatolik: {e}")

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )
