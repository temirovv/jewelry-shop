from django.db import migrations


DEFAULT_DATA = [
    {
        "name": "Toshkent shahri",
        "ordering": 1,
        "zones": [
            ("Yunusobod", 30000, 500000, "1 kun"),
            ("Chilonzor", 30000, 500000, "1 kun"),
            ("Mirzo Ulug'bek", 30000, 500000, "1 kun"),
            ("Shayxontohur", 30000, 500000, "1 kun"),
            ("Yakkasaroy", 30000, 500000, "1 kun"),
            ("Mirobod", 30000, 500000, "1 kun"),
            ("Olmazor", 30000, 500000, "1 kun"),
            ("Sergeli", 35000, 500000, "1-2 kun"),
            ("Uchtepa", 35000, 500000, "1-2 kun"),
            ("Yashnobod", 35000, 500000, "1-2 kun"),
            ("Bektemir", 40000, 500000, "1-2 kun"),
        ],
    },
    {
        "name": "Toshkent viloyati",
        "ordering": 2,
        "zones": [
            ("Chirchiq", 50000, 700000, "1-2 kun"),
            ("Angren", 60000, 700000, "2 kun"),
            ("Olmaliq", 60000, 700000, "2 kun"),
            ("Bekobod", 70000, 700000, "2-3 kun"),
            ("Yangiyo'l", 50000, 700000, "1-2 kun"),
            ("Boshqa tumanlar", 70000, 700000, "2-3 kun"),
        ],
    },
    {
        "name": "Samarqand",
        "ordering": 3,
        "zones": [
            ("Samarqand shahri", 80000, 1000000, "2-3 kun"),
            ("Viloyat tumanlari", 100000, 1000000, "3-4 kun"),
        ],
    },
    {
        "name": "Buxoro",
        "ordering": 4,
        "zones": [
            ("Buxoro shahri", 90000, 1000000, "3-4 kun"),
            ("Viloyat tumanlari", 110000, 1000000, "4-5 kun"),
        ],
    },
    {
        "name": "Andijon",
        "ordering": 5,
        "zones": [
            ("Andijon shahri", 90000, 1000000, "3-4 kun"),
            ("Viloyat tumanlari", 110000, 1000000, "4-5 kun"),
        ],
    },
    {
        "name": "Farg'ona",
        "ordering": 6,
        "zones": [
            ("Farg'ona shahri", 90000, 1000000, "3-4 kun"),
            ("Viloyat tumanlari", 110000, 1000000, "4-5 kun"),
        ],
    },
    {
        "name": "Namangan",
        "ordering": 7,
        "zones": [
            ("Namangan shahri", 90000, 1000000, "3-4 kun"),
            ("Viloyat tumanlari", 110000, 1000000, "4-5 kun"),
        ],
    },
    {
        "name": "Qashqadaryo",
        "ordering": 8,
        "zones": [
            ("Qarshi shahri", 100000, 1200000, "3-5 kun"),
            ("Viloyat tumanlari", 120000, 1200000, "4-5 kun"),
        ],
    },
    {
        "name": "Surxondaryo",
        "ordering": 9,
        "zones": [
            ("Termiz shahri", 120000, 1200000, "4-5 kun"),
            ("Viloyat tumanlari", 140000, 1200000, "5-6 kun"),
        ],
    },
    {
        "name": "Xorazm",
        "ordering": 10,
        "zones": [
            ("Urganch shahri", 120000, 1200000, "4-5 kun"),
            ("Viloyat tumanlari", 140000, 1200000, "5-6 kun"),
        ],
    },
    {
        "name": "Navoiy",
        "ordering": 11,
        "zones": [
            ("Navoiy shahri", 100000, 1100000, "3-4 kun"),
            ("Viloyat tumanlari", 120000, 1100000, "4-5 kun"),
        ],
    },
    {
        "name": "Jizzax",
        "ordering": 12,
        "zones": [
            ("Jizzax shahri", 80000, 1000000, "2-3 kun"),
            ("Viloyat tumanlari", 100000, 1000000, "3-4 kun"),
        ],
    },
    {
        "name": "Sirdaryo",
        "ordering": 13,
        "zones": [
            ("Guliston", 70000, 900000, "2-3 kun"),
            ("Viloyat tumanlari", 90000, 900000, "3-4 kun"),
        ],
    },
    {
        "name": "Qoraqalpog'iston",
        "ordering": 14,
        "zones": [
            ("Nukus shahri", 140000, 1500000, "5-6 kun"),
            ("Respublika tumanlari", 160000, 1500000, "6-7 kun"),
        ],
    },
]


def seed(apps, schema_editor):
    Region = apps.get_model("delivery", "Region")
    DeliveryZone = apps.get_model("delivery", "DeliveryZone")

    for region_data in DEFAULT_DATA:
        region, _ = Region.objects.get_or_create(
            name=region_data["name"],
            defaults={"ordering": region_data["ordering"], "is_active": True},
        )
        for idx, (name, fee, free_threshold, days) in enumerate(region_data["zones"]):
            DeliveryZone.objects.get_or_create(
                region=region,
                name=name,
                defaults={
                    "fee": fee,
                    "free_threshold": free_threshold,
                    "estimated_days": days,
                    "ordering": idx,
                    "is_active": True,
                },
            )


def unseed(apps, schema_editor):
    Region = apps.get_model("delivery", "Region")
    Region.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("delivery", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
