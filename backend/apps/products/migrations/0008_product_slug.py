import apps.products.models
from django.db import migrations, models


def fill_slugs(apps_registry, schema_editor):
    Product = apps_registry.get_model("products", "Product")
    for product in Product.objects.filter(slug__isnull=True).order_by("id"):
        product.slug = apps.products.models.build_product_slug(
            Product, product.name, exclude_pk=product.pk
        )
        product.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0007_alter_product_cost_price"),
    ]

    operations = [
        # 1) Avval bo'sh (NULL) ustun — mavjud mahsulotlarda unique buzilmasin
        migrations.AddField(
            model_name="product",
            name="slug",
            field=models.SlugField(
                allow_unicode=True, blank=True, max_length=280, null=True
            ),
        ),
        # 2) Mavjud mahsulotlarga nomdan slug yasash
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
    ]
