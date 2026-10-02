"""Mahsulot rasmlari uchun WebP thumbnail'lar.

Asl rasmlar (Telegram'dan olingan 200-500 KB JPEG) 150 px'lik kartochka
uchun ham to'liq yuklanardi. Thumbnail birinchi so'rovda yasaladi va
media/thumbs/<kenglik>/ ga saqlanadi — keyingi so'rovlar tayyorini oladi.
Model va migratsiya kerak emas.
"""
import logging
import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)

THUMB_WIDTH = 400  # kartochkalar (~160 px × 2.5 DPR)
LARGE_WIDTH = 1080  # mahsulot sahifasidagi galereya
WEBP_QUALITY = 80


def thumbnail_name(original_name: str, width: int) -> str:
    base, _ = os.path.splitext(original_name)
    return f"thumbs/{width}/{base}.webp"


def _render(image_file, width: int) -> bytes:
    with Image.open(image_file) as img:
        img = ImageOps.exif_transpose(img)
        has_alpha = img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        )
        img = img.convert("RGBA" if has_alpha else "RGB")
        # Faqat kichraytiriladi; kichik rasm kattalashtirilmaydi
        if img.width > width:
            height = round(img.height * width / img.width)
            img = img.resize((width, height), Image.LANCZOS)
        buf = BytesIO()
        img.save(buf, "WEBP", quality=WEBP_QUALITY, method=4)
        return buf.getvalue()


def get_thumbnail_url(image_field, width: int) -> str | None:
    """Thumbnail URL'i; yasab bo'lmasa None (frontend asl rasmga qaytadi)."""
    if not image_field:
        return None

    storage = image_field.storage
    name = thumbnail_name(image_field.name, width)
    if not storage.exists(name):
        try:
            with image_field.open("rb") as f:
                data = _render(f, width)
            # Ikki worker bir vaqtda yasasa, ikkinchisi suffix'li nom oladi —
            # zarari yo'q, URL baribir asosiy nomga ishora qiladi
            storage.save(name, ContentFile(data))
        except Exception:
            logger.exception("Thumbnail yasab bo'lmadi: %s", image_field.name)
            return None
    return storage.url(name)
