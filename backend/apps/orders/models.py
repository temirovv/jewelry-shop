import secrets

from django.core.validators import MaxValueValidator
from django.db import models
from apps.users.models import TelegramUser
from apps.products.models import Product


# 0/O va 1/I kabi adashtiriladigan belgilarsiz — mijoz raqamni telefonda
# aytib berganda xato bo'lmasin
ORDER_NUMBER_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
ORDER_NUMBER_PREFIX = "ZY-"
ORDER_NUMBER_LENGTH = 6


def generate_order_number():
    return ORDER_NUMBER_PREFIX + "".join(
        secrets.choice(ORDER_NUMBER_ALPHABET) for _ in range(ORDER_NUMBER_LENGTH)
    )


class Order(models.Model):
    """Buyurtma"""

    STATUS_CHOICES = [
        ("pending", "Kutilmoqda"),
        ("confirmed", "Tasdiqlangan"),
        ("processing", "Tayyorlanmoqda"),
        ("shipped", "Jo'natilgan"),
        ("delivered", "Yetkazilgan"),
        ("cancelled", "Bekor qilingan"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Naqd pul"),
        ("transfer", "Karta o'tkazma"),
    ]

    # Tashqariga ko'rinadigan raqam. Ketma-ket id mijozga ko'rsatilsa,
    # istalgan kishi bitta buyurtma berib, do'kon savdo hajmini bilib oladi.
    number = models.CharField(
        max_length=16, unique=True, editable=False, verbose_name="Buyurtma raqami"
    )
    user = models.ForeignKey(
        TelegramUser, on_delete=models.PROTECT, related_name="orders"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    delivery_zone = models.ForeignKey(
        "delivery.DeliveryZone",
        on_delete=models.PROTECT,
        related_name="orders",
        null=True,
        blank=True,
        verbose_name="Yetkazish zonasi",
    )
    delivery_fee = models.DecimalField(
        max_digits=12, decimal_places=0, default=0, verbose_name="Yetkazish narxi"
    )

    # To'lov ma'lumotlari
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="cash",
        verbose_name="To'lov usuli",
    )
    is_paid = models.BooleanField(default=False, verbose_name="To'langan")

    phone = models.CharField(max_length=20)
    delivery_address = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.number} - {self.user.full_name}"

    def save(self, *args, **kwargs):
        if not self.number:
            number = generate_order_number()
            while Order.objects.filter(number=number).exists():
                number = generate_order_number()
            self.number = number
        super().save(*args, **kwargs)

    def calculate_total(self):
        items_total = sum(item.subtotal for item in self.items.all())
        self.total = items_total + self.delivery_fee
        self.save(update_fields=["total"])


class OrderItem(models.Model):
    """Buyurtma elementi"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(99)])
    price = models.DecimalField(max_digits=12, decimal_places=0)
    cost_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="Tannarx",
        help_text="Buyurtma paytidagi tannarx (muzlatilgan)",
    )
    size = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Buyurtma elementi"
        verbose_name_plural = "Buyurtma elementlari"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        if self.price is None or self.quantity is None:
            return 0
        return self.price * self.quantity

    @property
    def profit(self):
        """Ushbu element bo'yicha yalpi foyda ((sotuv − tannarx) × miqdor)."""
        if self.price is None or self.quantity is None:
            return 0
        return (self.price - (self.cost_price or 0)) * self.quantity

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.product.price
        if not self.cost_price and self.product_id:
            self.cost_price = self.product.cost_price
        super().save(*args, **kwargs)
