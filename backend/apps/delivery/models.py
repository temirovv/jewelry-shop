from django.db import models


class Region(models.Model):
    """Viloyat / Shahar"""

    name = models.CharField(max_length=100, unique=True, verbose_name="Nomi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    ordering = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"
        ordering = ["ordering", "name"]

    def __str__(self):
        return self.name


class DeliveryZone(models.Model):
    """Yetkazib berish zonasi (tuman / rayon)"""

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="zones",
        verbose_name="Viloyat",
    )
    name = models.CharField(max_length=100, verbose_name="Zona / Tuman")
    fee = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="Yetkazish narxi",
    )
    free_threshold = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="Bepul yetkazish chegarasi",
        help_text="Buyurtma shu summadan oshsa, yetkazish bepul. 0 — har doim to'lanadi.",
    )
    estimated_days = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Yetkazish muddati",
        help_text="Masalan: 1-2 kun",
    )
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    ordering = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        verbose_name = "Yetkazish zonasi"
        verbose_name_plural = "Yetkazish zonalari"
        ordering = ["region__ordering", "ordering", "name"]
        unique_together = [("region", "name")]

    def __str__(self):
        return f"{self.region.name} — {self.name}"

    def calculate_fee(self, order_total):
        """Buyurtma summasiga qarab yetkazish narxini hisoblash."""
        if self.free_threshold and order_total >= self.free_threshold:
            return 0
        return self.fee
