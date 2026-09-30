import apps.products.models
from django.db import migrations, models


# Alohida migratsiya: Postgres'da qatorlarni yangilash va ALTER TABLE bitta
# tranzaksiyada bo'lsa "pending trigger events" xatosi chiqishi mumkin.
class Migration(migrations.Migration):
    dependencies = [
        ("products", "0008_product_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(
                allow_unicode=True,
                blank=True,
                help_text="URL uchun. Bo'sh qoldirilsa nomdan yasaladi; keyin o'zgartirilsa eski havolalar ishlamay qoladi.",
                max_length=280,
                unique=True,
                validators=[apps.products.models.validate_not_numeric],
            ),
        ),
    ]
