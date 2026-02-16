import logging
import httpx
from django.conf import settings

from .models import Order

logger = logging.getLogger(__name__)


def get_pending_orders_count(request):
    """Return pending orders count for sidebar badge."""
    count = Order.objects.filter(status="pending").count()
    return count if count > 0 else None


def send_order_notification(order: Order):
    """Yangi buyurtma haqida admin userlarga Telegram orqali xabar yuborish."""
    bot_token = getattr(settings, "BOT_TOKEN", None)
    admin_ids = getattr(settings, "ADMIN_IDS", [])

    if not bot_token or not admin_ids:
        logger.warning("BOT_TOKEN yoki ADMIN_IDS sozlanmagan")
        return

    # Buyurtma ma'lumotlarini tayyorlash
    items_text = "\n".join(
        f"  • {item.product.name} x{item.quantity} — {item.price:,.0f} so'm"
        for item in order.items.all()
    )

    payment_method = order.get_payment_method_display()

    message = f"""
🛍 <b>Yangi buyurtma #{order.id:05d}</b>

👤 <b>Mijoz:</b> {order.user.first_name or 'Noma\'lum'}
📱 <b>Telefon:</b> {order.phone}
💳 <b>To'lov:</b> {payment_method}

📦 <b>Mahsulotlar:</b>
{items_text}

💰 <b>Jami:</b> {order.total:,.0f} so'm
"""

    if order.delivery_address:
        message += f"\n📍 <b>Manzil:</b> {order.delivery_address}"

    if order.comment:
        message += f"\n💬 <b>Izoh:</b> {order.comment}"

    # Har bir admin userga xabar yuborish
    for admin_id in admin_ids:
        _send_telegram_message(bot_token, admin_id, message)


def send_status_notification(order: Order, new_status: str):
    """Buyurtma holati o'zgarganda foydalanuvchiga Telegram orqali xabar yuborish."""
    bot_token = getattr(settings, "BOT_TOKEN", None)
    if not bot_token:
        return

    STATUS_LABELS = {
        "pending": "⏳ Kutilmoqda",
        "confirmed": "✅ Tasdiqlangan",
        "processing": "🔄 Tayyorlanmoqda",
        "shipped": "🚚 Yo'lda",
        "delivered": "📦 Yetkazildi",
        "cancelled": "❌ Bekor qilingan",
    }

    STATUS_MESSAGES = {
        "confirmed": "Buyurtmangiz tasdiqlandi! Tez orada tayyorlaymiz.",
        "processing": "Buyurtmangiz tayyorlanmoqda...",
        "shipped": "Buyurtmangiz yo'lga chiqdi!",
        "delivered": "Buyurtmangiz yetkazildi! Xaridingiz uchun rahmat!",
        "cancelled": "Buyurtmangiz bekor qilindi.",
    }

    status_label = STATUS_LABELS.get(new_status, new_status)
    extra_msg = STATUS_MESSAGES.get(new_status, "")
    total_formatted = f"{order.total:,.0f}".replace(",", " ")

    message = (
        f"🔔 <b>Buyurtma yangilandi!</b>\n\n"
        f"🛍 Buyurtma: <b>#{order.id:05d}</b>\n"
        f"📋 Yangi holat: <b>{status_label}</b>\n"
        f"💰 Summa: <b>{total_formatted} so'm</b>\n"
    )
    if extra_msg:
        message += f"\n{extra_msg}"

    telegram_id = order.user.telegram_id
    _send_telegram_message(bot_token, telegram_id, message)


def _send_telegram_message(bot_token: str, chat_id: int, text: str):
    """Telegram API orqali xabar yuborish."""
    try:
        with httpx.Client(timeout=10) as client:
            response = client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                },
            )
            if response.status_code != 200:
                logger.error(f"Telegram xabar yuborishda xatolik: {response.text}")
    except Exception as e:
        logger.error(f"Telegram xabar yuborishda xatolik (chat_id={chat_id}): {e}")
