from django.db import models
from django.utils.text import slugify


class Banner(models.Model):
    """Bosh sahifa carousel bannerlari"""

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    emoji = models.CharField(max_length=10, default="💎", help_text="Banner emoji")
    gradient = models.CharField(
        max_length=200,
        default="from-amber-500/20 via-amber-600/10 to-transparent",
        help_text="Tailwind gradient classlari"
    )
    link = models.CharField(max_length=200, blank=True, help_text="Bosilganda o'tish linki")
    image = models.ImageField(upload_to="banners/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Bannerlar"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title


class Category(models.Model):
    """Mahsulot kategoriyasi"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField(max_length=10, blank=True, help_text="Emoji")
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Zargarlik buyumi"""

    METAL_TYPES = [
        ("gold", "Oltin"),
        ("silver", "Kumush"),
        ("platinum", "Platina"),
        ("white_gold", "Oq oltin"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    old_price = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    metal_type = models.CharField(max_length=20, choices=METAL_TYPES, default="gold")
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Gramm")
    size = models.CharField(max_length=50, blank=True)
    proba = models.CharField(max_length=10, default="585", help_text="585, 750, 925 va h.k.")

    in_stock = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Bosh sahifada ko'rsatish")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    @property
    def main_image(self):
        main = self.images.filter(is_main=True).first()
        if not main:
            main = self.images.first()
        if main:
            if main.image:
                return main.image.url
            if main.image_url:
                return main.image_url
        return None


class ProductImage(models.Model):
    """Mahsulot rasmi"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="Tashqi rasm URL")
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Mahsulot rasmi"
        verbose_name_plural = "Mahsulot rasmlari"
        ordering = ["order"]

    def __str__(self):
        return f"{self.product.name} - Rasm {self.id}"

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(
                product=self.product, is_main=True
            ).update(is_main=False)
        super().save(*args, **kwargs)
