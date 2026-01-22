from django.core.management.base import BaseCommand
from apps.products.models import Product, ProductImage


# Unsplash zargarlik rasmlari (Unsplash Source API)
JEWELRY_IMAGES = {
    "rings": [
        "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=800&q=80",
        "https://images.unsplash.com/photo-1602751584552-8ba73aad10e1?w=800&q=80",
        "https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=800&q=80",
        "https://images.unsplash.com/photo-1611652022419-a9419f74343d?w=800&q=80",
    ],
    "earrings": [
        "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&q=80",
        "https://images.unsplash.com/photo-1588444837495-c6cfeb53f32d?w=800&q=80",
        "https://images.unsplash.com/photo-1630019852942-f89202989a59?w=800&q=80",
    ],
    "necklaces": [
        "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=800&q=80",
        "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&q=80",
        "https://images.unsplash.com/photo-1611085583191-a3b181a88401?w=800&q=80",
        "https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=800&q=80",
    ],
    "bracelets": [
        "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800&q=80",
        "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800&q=80",
        "https://images.unsplash.com/photo-1620000617482-821324eb9a14?w=800&q=80",
    ],
    "sets": [
        "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&q=80",
        "https://images.unsplash.com/photo-1617038220319-276d3cfab638?w=800&q=80",
    ],
    "watches": [
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80",
        "https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?w=800&q=80",
    ],
}


class Command(BaseCommand):
    help = "Mahsulotlarga test rasmlarini qo'shish"

    def handle(self, *args, **options):
        self.stdout.write("Rasmlar qo'shilmoqda...")

        # Har bir kategoriya uchun
        category_images = {
            "rings": 0,
            "earrings": 0,
            "necklaces": 0,
            "bracelets": 0,
            "sets": 0,
            "watches": 0,
        }

        products = Product.objects.all()
        images_added = 0

        for product in products:
            # Agar rasm bor bo'lsa, o'tkazib yuborish
            if product.images.exists():
                continue

            category_slug = product.category.slug

            if category_slug in JEWELRY_IMAGES:
                images = JEWELRY_IMAGES[category_slug]
                index = category_images[category_slug] % len(images)
                image_url = images[index]
                category_images[category_slug] += 1

                # Asosiy rasm qo'shish
                ProductImage.objects.create(
                    product=product,
                    image_url=image_url,
                    is_main=True,
                    order=0,
                )
                images_added += 1
                self.stdout.write(f"  + {product.name}: {image_url[:50]}...")

        self.stdout.write(
            self.style.SUCCESS(f"\n{images_added} ta rasm qo'shildi!")
        )
