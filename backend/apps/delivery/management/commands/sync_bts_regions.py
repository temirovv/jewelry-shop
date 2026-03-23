from django.core.management.base import BaseCommand

from apps.delivery.services import sync_regions_and_cities


class Command(BaseCommand):
    help = "BTS API dan regionlar va shaharlarni DB ga yuklash"

    def handle(self, *args, **options):
        self.stdout.write("BTS regionlarni sinxronlash boshlandi...")
        try:
            regions, cities = sync_regions_and_cities()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Muvaffaqiyatli: {regions} ta viloyat, {cities} ta shahar sinxronlandi."
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Xatolik: {e}"))
