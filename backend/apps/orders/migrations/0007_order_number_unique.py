from django.db import migrations, models


# Alohida migratsiya: Postgres'da qatorlarni yangilash va ALTER TABLE bitta
# tranzaksiyada bo'lsa "pending trigger events" xatosi chiqishi mumkin.
class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0006_order_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="number",
            field=models.CharField(
                editable=False, max_length=16, unique=True, verbose_name="Buyurtma raqami"
            ),
        ),
    ]
