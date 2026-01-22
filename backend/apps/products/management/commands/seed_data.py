from django.core.management.base import BaseCommand
from apps.products.models import Category, Product, ProductImage


class Command(BaseCommand):
    help = "Test ma'lumotlarni yaratish"

    def handle(self, *args, **options):
        self.stdout.write("Ma'lumotlar yaratilmoqda...")

        # Kategoriyalar
        categories_data = [
            {"name": "Uzuklar", "slug": "rings", "icon": "💍", "order": 1},
            {"name": "Sirg'alar", "slug": "earrings", "icon": "✨", "order": 2},
            {"name": "Marjonlar", "slug": "necklaces", "icon": "📿", "order": 3},
            {"name": "Bilaguzuklar", "slug": "bracelets", "icon": "⌚", "order": 4},
            {"name": "To'plamlar", "slug": "sets", "icon": "🎁", "order": 5},
            {"name": "Soatlar", "slug": "watches", "icon": "⏰", "order": 6},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data["slug"],
                defaults=cat_data
            )
            categories[cat_data["slug"]] = cat
            status = "yaratildi" if created else "mavjud"
            self.stdout.write(f"  Kategoriya: {cat.name} - {status}")

        # Mahsulotlar
        products_data = [
            {
                "name": "Oltin uzuk 585 proba, brilliant bilan",
                "description": "Klassik dizayndagi oltin uzuk. 585 proba sof oltin, markazida 0.5 karatli brilliant. Har qanday tantanali marosim uchun ideal tanlov.",
                "price": 2500000,
                "old_price": 3000000,
                "category": "rings",
                "metal_type": "gold",
                "weight": 3.5,
                "size": "17",
                "proba": "585",
                "is_featured": True,
            },
            {
                "name": "Nikoh uzugi klassik",
                "description": "Sodda va nafis nikoh uzugi. 585 proba oltin, ichki qismida isim yozish mumkin.",
                "price": 1800000,
                "category": "rings",
                "metal_type": "gold",
                "weight": 2.8,
                "size": "16-22",
                "proba": "585",
                "is_featured": False,
            },
            {
                "name": "Sirg'a to'plami, marvarid bilan",
                "description": "Tabiiy dengiz marvaridi bilan bezatilgan sirg'alar. 585 proba oltin, marvarid diametri 8mm.",
                "price": 1800000,
                "category": "earrings",
                "metal_type": "gold",
                "weight": 2.8,
                "proba": "585",
                "is_featured": True,
            },
            {
                "name": "Osilib turadigan sirg'alar",
                "description": "Zamonaviy dizayn, 585 proba oltin. Har qanday libosga mos keladi.",
                "price": 2200000,
                "old_price": 2500000,
                "category": "earrings",
                "metal_type": "gold",
                "weight": 4.2,
                "proba": "585",
                "is_featured": False,
            },
            {
                "name": "Marjon zanjir, italyan to'qish",
                "description": "Italiya ishlab chiqarishi, 585 proba oltin. Uzunligi 45sm, kengaytirilishi mumkin.",
                "price": 4200000,
                "old_price": 4800000,
                "category": "necklaces",
                "metal_type": "gold",
                "weight": 8.2,
                "proba": "585",
                "is_featured": True,
            },
            {
                "name": "Marjon kulon bilan",
                "description": "Yurak shaklidagi kulon, 585 proba oltin. Ichiga rasm qo'yish mumkin.",
                "price": 3500000,
                "category": "necklaces",
                "metal_type": "gold",
                "weight": 6.5,
                "proba": "585",
                "is_featured": False,
            },
            {
                "name": "Bilaguzuk, oltin 585",
                "description": "Zamonaviy dizayn, 585 proba oltin. Uzunligi sozlanadi.",
                "price": 3100000,
                "category": "bracelets",
                "metal_type": "gold",
                "weight": 5.4,
                "proba": "585",
                "is_featured": False,
            },
            {
                "name": "Tennis bilaguzuk brilliant bilan",
                "description": "Klassik tennis bilaguzuk, 585 proba oltin, 2 karat umumiy brilliant vazni.",
                "price": 8500000,
                "old_price": 9500000,
                "category": "bracelets",
                "metal_type": "gold",
                "weight": 12.0,
                "proba": "585",
                "is_featured": True,
            },
            {
                "name": "To'plam: uzuk + sirg'a",
                "description": "Bir xil dizayndagi uzuk va sirg'a to'plami. 585 proba oltin, brilliant bilan.",
                "price": 4500000,
                "old_price": 5200000,
                "category": "sets",
                "metal_type": "gold",
                "weight": 7.5,
                "proba": "585",
                "is_featured": True,
            },
            {
                "name": "Kumush uzuk 925",
                "description": "925 proba kumush, zirkon tosh bilan. Arzon narxda sifatli zargarlik.",
                "price": 450000,
                "category": "rings",
                "metal_type": "silver",
                "weight": 4.0,
                "size": "16-20",
                "proba": "925",
                "is_featured": False,
            },
            {
                "name": "Oq oltin uzuk",
                "description": "750 proba oq oltin, safir tosh bilan. Premium segment.",
                "price": 6500000,
                "category": "rings",
                "metal_type": "white_gold",
                "weight": 4.5,
                "size": "17",
                "proba": "750",
                "is_featured": True,
            },
            {
                "name": "Erkaklar uchun zanjir",
                "description": "585 proba oltin, bismark to'qish. Uzunligi 55sm.",
                "price": 7800000,
                "category": "necklaces",
                "metal_type": "gold",
                "weight": 15.0,
                "proba": "585",
                "is_featured": False,
            },
        ]

        for prod_data in products_data:
            category_slug = prod_data.pop("category")
            category = categories.get(category_slug)

            if not category:
                self.stdout.write(f"  Kategoriya topilmadi: {category_slug}")
                continue

            product, created = Product.objects.get_or_create(
                name=prod_data["name"],
                defaults={**prod_data, "category": category}
            )
            status = "yaratildi" if created else "mavjud"
            self.stdout.write(f"  Mahsulot: {product.name[:40]}... - {status}")

        self.stdout.write(self.style.SUCCESS(
            f"\nMuvaffaqiyatli! {Category.objects.count()} kategoriya, "
            f"{Product.objects.count()} mahsulot bazada."
        ))
