from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=0, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price", "size", "subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    payment_method_display = serializers.CharField(
        source="get_payment_method_display", read_only=True
    )
    delivery_zone_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "status_display",
            "total",
            "delivery_zone",
            "delivery_zone_name",
            "delivery_fee",
            "phone",
            "delivery_address",
            "comment",
            "payment_method",
            "payment_method_display",
            "is_paid",
            "items",
            "created_at",
        ]
        read_only_fields = [
            "id", "status", "total", "delivery_fee", "is_paid", "created_at",
        ]

    def get_delivery_zone_name(self, obj):
        if obj.delivery_zone:
            return f"{obj.delivery_zone.region.name} — {obj.delivery_zone.name}"
        return None


class CreateOrderSerializer(serializers.Serializer):
    """Buyurtma yaratish uchun"""

    items = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
    )
    phone = serializers.CharField(max_length=20)
    delivery_address = serializers.CharField(
        required=False, allow_blank=True, max_length=500
    )
    delivery_zone_id = serializers.IntegerField(required=False, allow_null=True)
    comment = serializers.CharField(
        required=False, allow_blank=True, max_length=500
    )
    payment_method = serializers.ChoiceField(
        choices=["cash", "transfer"],
        default="cash",
    )

    def validate_phone(self, value):
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) < 9 or len(digits) > 12:
            raise serializers.ValidationError(
                "Telefon raqam 9–12 ta raqamdan iborat bo'lishi kerak"
            )
        return value.strip()

    def validate_delivery_zone_id(self, value):
        if value is None:
            return value
        from apps.delivery.models import DeliveryZone

        if not DeliveryZone.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Yetkazish zonasi topilmadi")
        return value

    def validate_items(self, value):
        from apps.products.models import Product

        for item in value:
            if "product_id" not in item or "quantity" not in item:
                raise serializers.ValidationError(
                    "Har bir element 'product_id' va 'quantity' bo'lishi kerak"
                )
            try:
                qty = int(item["quantity"])
            except (TypeError, ValueError):
                raise serializers.ValidationError("Miqdor butun son bo'lishi kerak")
            if qty < 1 or qty > 99:
                raise serializers.ValidationError(
                    "Miqdor 1 dan 99 gacha bo'lishi kerak"
                )
            if not Product.objects.filter(id=item["product_id"], is_active=True).exists():
                raise serializers.ValidationError(
                    f"Mahsulot #{item['product_id']} topilmadi"
                )
        return value
