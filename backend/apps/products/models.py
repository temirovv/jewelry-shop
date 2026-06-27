from django.db import models, transaction
from django.utils.text import slugify


class Banner(models.Model):
    """Bosh sahifa carousel bannerlari"""

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    emoji = models.CharField(max_length=10, default="💄", help_text="Banner emoji")
    gradient = models.CharField(
        max_length=200,
        default="from-pink-500/20 via-rose-400/10 to-transparent",
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
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """Kosmetika brendi"""

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)
    country = models.CharField(max_length=80, blank=True, help_text="Ishlab chiqaruvchi davlat")
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False, help_text="Bosh sahifada ko'rsatish")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Brend"
        verbose_name_plural = "Brendlar"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Kosmetika mahsuloti"""

    PRODUCT_TYPES = [
        ("skincare", "Teri parvarishi"),
        ("makeup", "Makiyaj"),
        ("perfume", "Parfyumeriya"),
        ("haircare", "Soch parvarishi"),
        ("bodycare", "Tana parvarishi"),
    ]

    SKIN_TYPES = [
        ("all", "Barcha teri turlari"),
        ("dry", "Quruq"),
        ("oily", "Yog'li"),
        ("combination", "Aralash"),
        ("normal", "Normal"),
        ("sensitive", "Sezgir"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    old_price = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, related_name="products", null=True, blank=True
    )
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default="skincare")
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPES, default="all", blank=True)
    volume = models.CharField(max_length=50, blank=True, help_text="Hajm, masalan 50 ml")
    shade = models.CharField(max_length=80, blank=True, help_text="Rang/ton, masalan 'Nude 02'")
    ingredients = models.TextField(blank=True, help_text="Asosiy tarkib")
    shelf_life_months = models.PositiveIntegerField(
        blank=True, null=True, help_text="Yaroqlilik muddati (oy)"
    )
    country_of_origin = models.CharField(max_length=80, blank=True)

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
        if main and main.image:
            return main.image.url
        return None


class ProductImage(models.Model):
    """Mahsulot rasmi"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Mahsulot rasmi"
        verbose_name_plural = "Mahsulot rasmlari"
        ordering = ["order"]

    def __str__(self):
        return f"{self.product.name} - Rasm {self.id}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_main:
                ProductImage.objects.filter(
                    product=self.product, is_main=True
                ).update(is_main=False)
            super().save(*args, **kwargs)
