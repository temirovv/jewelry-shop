from django.core.management.base import BaseCommand
from apps.products.models import Brand, Category, Product


class Command(BaseCommand):
    help = "Test ma'lumotlarni yaratish (kosmetika)"

    def handle(self, *args, **options):
        self.stdout.write("Ma'lumotlar yaratilmoqda...")

        # Kategoriyalar
        categories_data = [
            {"name": "Teri parvarishi", "slug": "skincare", "icon": "🧴", "order": 1},
            {"name": "Makiyaj", "slug": "makeup", "icon": "💄", "order": 2},
            {"name": "Parfyumeriya", "slug": "perfume", "icon": "🌸", "order": 3},
            {"name": "Soch parvarishi", "slug": "haircare", "icon": "💆", "order": 4},
            {"name": "Tana parvarishi", "slug": "bodycare", "icon": "🧼", "order": 5},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data["slug"], defaults=cat_data
            )
            categories[cat_data["slug"]] = cat
            status = "yaratildi" if created else "mavjud"
            self.stdout.write(f"  Kategoriya: {cat.name} - {status}")

        # Brendlar
        brands_data = [
            {"name": "L'Oréal Paris", "slug": "loreal", "country": "Fransiya", "is_featured": True, "order": 1},
            {"name": "Maybelline", "slug": "maybelline", "country": "AQSH", "is_featured": True, "order": 2},
            {"name": "The Ordinary", "slug": "the-ordinary", "country": "Kanada", "is_featured": True, "order": 3},
            {"name": "CeraVe", "slug": "cerave", "country": "AQSH", "is_featured": True, "order": 4},
            {"name": "Nivea", "slug": "nivea", "country": "Germaniya", "is_featured": False, "order": 5},
            {"name": "Garnier", "slug": "garnier", "country": "Fransiya", "is_featured": False, "order": 6},
            {"name": "Dior", "slug": "dior", "country": "Fransiya", "is_featured": True, "order": 7},
        ]

        brands = {}
        for b_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                slug=b_data["slug"], defaults=b_data
            )
            brands[b_data["slug"]] = brand
            status = "yaratildi" if created else "mavjud"
            self.stdout.write(f"  Brend: {brand.name} - {status}")

        # Mahsulotlar
        products_data = [
            {
                "name": "Revitalift namlovchi yuz kremi",
                "description": "Hyaluron kislotasi bilan namlovchi va yoshartiruvchi yuz kremi. Quruq va aralash teri uchun ideal.",
                "price": 185000, "old_price": 230000,
                "category": "skincare", "brand": "loreal",
                "product_type": "skincare", "skin_type": "dry",
                "volume": "50 ml", "country_of_origin": "Fransiya",
                "shelf_life_months": 24, "is_featured": True,
            },
            {
                "name": "Niacinamide 10% + Zinc 1% serum",
                "description": "Yog' ajralishini muvozanatlaydigan va teri tonusini tekislaydigan serum. Yog'li va muammoli teri uchun.",
                "price": 95000,
                "category": "skincare", "brand": "the-ordinary",
                "product_type": "skincare", "skin_type": "oily",
                "volume": "30 ml", "country_of_origin": "Kanada",
                "shelf_life_months": 12, "is_featured": True,
            },
            {
                "name": "CeraVe namlovchi losyon",
                "description": "Seramidlar va hyaluron kislotasi bilan teri to'sig'ini tiklaydigan losyon. Sezgir teri uchun.",
                "price": 145000, "old_price": 170000,
                "category": "skincare", "brand": "cerave",
                "product_type": "skincare", "skin_type": "sensitive",
                "volume": "236 ml", "country_of_origin": "AQSH",
                "shelf_life_months": 24, "is_featured": True,
            },
            {
                "name": "Maybelline Fit Me tonal krem",
                "description": "Tabiiy ko'rinish beruvchi, teriga mos keluvchi tonal asos. SPF 18 bilan.",
                "price": 120000,
                "category": "makeup", "brand": "maybelline",
                "product_type": "makeup", "skin_type": "all",
                "volume": "30 ml", "shade": "220 Natural Beige",
                "country_of_origin": "AQSH", "shelf_life_months": 36, "is_featured": True,
            },
            {
                "name": "Maybelline Lash Sensational tush",
                "description": "Kipriklarga hajm va uzunlik beruvchi tush. Suvga chidamli formula.",
                "price": 110000, "old_price": 135000,
                "category": "makeup", "brand": "maybelline",
                "product_type": "makeup", "skin_type": "all",
                "volume": "9.5 ml", "shade": "Qora",
                "country_of_origin": "AQSH", "shelf_life_months": 24, "is_featured": False,
            },
            {
                "name": "L'Oréal Color Riche lab bo'yog'i",
                "description": "Nam va to'yingan ranglarga ega lab bo'yog'i. Argan moyi bilan.",
                "price": 98000,
                "category": "makeup", "brand": "loreal",
                "product_type": "makeup", "skin_type": "all",
                "volume": "4.8 g", "shade": "Nude 235",
                "country_of_origin": "Fransiya", "shelf_life_months": 36, "is_featured": True,
            },
            {
                "name": "Dior Sauvage parfyum suvi",
                "description": "Yangi va o'ziga jalb qiluvchi erkaklar atiri. Bergamot va ambroksan notalari.",
                "price": 1450000, "old_price": 1650000,
                "category": "perfume", "brand": "dior",
                "product_type": "perfume", "skin_type": "all",
                "volume": "100 ml", "country_of_origin": "Fransiya",
                "shelf_life_months": 60, "is_featured": True,
            },
            {
                "name": "Miss Dior parfyum suvi",
                "description": "Gul notalariga boy ayollar atiri. Atirgul va peoniya ohanglari.",
                "price": 1380000,
                "category": "perfume", "brand": "dior",
                "product_type": "perfume", "skin_type": "all",
                "volume": "100 ml", "country_of_origin": "Fransiya",
                "shelf_life_months": 60, "is_featured": False,
            },
            {
                "name": "Garnier Fructis tiklovchi shampun",
                "description": "Zaiflashgan sochlarni mustahkamlaydigan va tiklaydigan shampun.",
                "price": 65000,
                "category": "haircare", "brand": "garnier",
                "product_type": "haircare", "skin_type": "all",
                "volume": "400 ml", "country_of_origin": "Fransiya",
                "shelf_life_months": 30, "is_featured": False,
            },
            {
                "name": "L'Oréal Elseve soch niqobi",
                "description": "Quruq va shikastlangan sochlar uchun intensiv namlovchi niqob.",
                "price": 78000, "old_price": 92000,
                "category": "haircare", "brand": "loreal",
                "product_type": "haircare", "skin_type": "all",
                "volume": "300 ml", "country_of_origin": "Fransiya",
                "shelf_life_months": 24, "is_featured": False,
            },
            {
                "name": "Nivea namlovchi tana suti",
                "description": "Quruq teri uchun 48 soatlik namlik beruvchi tana suti.",
                "price": 72000,
                "category": "bodycare", "brand": "nivea",
                "product_type": "bodycare", "skin_type": "dry",
                "volume": "400 ml", "country_of_origin": "Germaniya",
                "shelf_life_months": 36, "is_featured": True,
            },
            {
                "name": "Nivea Men yuz yuvish geli",
                "description": "Erkaklar uchun teri tozalaydigan va tetiklashtiradigan gel.",
                "price": 58000,
                "category": "skincare", "brand": "nivea",
                "product_type": "skincare", "skin_type": "normal",
                "volume": "100 ml", "country_of_origin": "Germaniya",
                "shelf_life_months": 24, "is_featured": False,
            },
        ]

        for prod_data in products_data:
            category = categories.get(prod_data.pop("category"))
            brand = brands.get(prod_data.pop("brand"))
            if not category:
                continue
            Product.objects.get_or_create(
                name=prod_data["name"],
                defaults={**prod_data, "category": category, "brand": brand},
            )
            self.stdout.write(f"  Mahsulot: {prod_data['name'][:40]}...")

        self.stdout.write(self.style.SUCCESS(
            f"\nMuvaffaqiyatli! {Category.objects.count()} kategoriya, "
            f"{Brand.objects.count()} brend, {Product.objects.count()} mahsulot bazada."
        ))
