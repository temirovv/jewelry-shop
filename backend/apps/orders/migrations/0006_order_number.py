from django.db import migrations, models

from apps.orders.models import generate_order_number


def fill_numbers(apps_registry, schema_editor):
    Order = apps_registry.get_model("orders", "Order")
    used = set()
    for order in Order.objects.filter(number__isnull=True).order_by("id"):
        number = generate_order_number()
        while number in used:
            number = generate_order_number()
        used.add(number)
        order.number = number
        order.save(update_fields=["number"])


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0005_orderitem_cost_price"),
    ]

    operations = [
        # 1) Avval bo'sh (NULL) ustun — mavjud buyurtmalarda unique buzilmasin
        migrations.AddField(
            model_name="order",
            name="number",
            field=models.CharField(
                editable=False, max_length=16, null=True, verbose_name="Buyurtma raqami"
            ),
        ),
        # 2) Mavjud buyurtmalarga tasodifiy raqam berish
        migrations.RunPython(fill_numbers, migrations.RunPython.noop),
    ]
