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

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "status_display",
            "total",
            "phone",
            "delivery_address",
            "comment",
            "payment_method",
            "payment_method_display",
            "is_paid",
            "items",
            "created_at",
        ]
        read_only_fields = ["id", "status", "total", "is_paid", "created_at"]


class CreateOrderSerializer(serializers.Serializer):
    """Buyurtma yaratish uchun"""

    items = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
    )
    phone = serializers.CharField(max_length=20)
    delivery_address = serializers.CharField(required=False, allow_blank=True)
    comment = serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(
        choices=["cash", "transfer"],
        default="cash",
    )

    def validate_items(self, value):
        from apps.products.models import Product

        for item in value:
            if "product_id" not in item or "quantity" not in item:
                raise serializers.ValidationError(
                    "Har bir element 'product_id' va 'quantity' bo'lishi kerak"
                )
            if not Product.objects.filter(id=item["product_id"], is_active=True).exists():
                raise serializers.ValidationError(
                    f"Mahsulot #{item['product_id']} topilmadi"
                )
        return value
