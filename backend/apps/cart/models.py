from django.db import models
from django.db.models import F, Sum
from apps.users.models import TelegramUser
from apps.products.models import Product


class Cart(models.Model):
    """Foydalanuvchi savati"""

    user = models.OneToOneField(
        TelegramUser, on_delete=models.CASCADE, related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Savat"
        verbose_name_plural = "Savatlar"

    def __str__(self):
        return f"Savat - {self.user.full_name}"

    @property
    def total(self):
        result = self.items.aggregate(
            total=Sum(F("product__price") * F("quantity"))
        )["total"]
        return result or 0

    @property
    def items_count(self):
        result = self.items.aggregate(total=Sum("quantity"))["total"]
        return result or 0


class CartItem(models.Model):
    """Savat elementi"""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Savat elementi"
        verbose_name_plural = "Savat elementlari"
        unique_together = ["cart", "product", "size"]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity
