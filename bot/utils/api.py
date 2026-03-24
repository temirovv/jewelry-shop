import logging
import aiohttp
from config import API_BASE_URL, BOT_TOKEN

logger = logging.getLogger(__name__)

STATUS_LABELS = {
    "pending": "\u23f3 Kutilmoqda",
    "confirmed": "\u2705 Tasdiqlangan",
    "processing": "\U0001f504 Tayyorlanmoqda",
    "shipped": "\U0001f69a Yo'lda",
    "delivered": "\U0001f4e6 Yetkazildi",
    "cancelled": "\u274c Bekor qilingan",
}

PAYMENT_LABELS = {
    "cash": "\U0001f4b5 Naqd pul",
    "transfer": "\U0001f4b3 Karta o'tkazma",
}


def _get_bot_headers(telegram_id: int) -> dict:
    """Bot API so'rovlari uchun auth headerlar."""
    return {
        "X-Bot-Token": BOT_TOKEN,
        "X-Telegram-User-Id": str(telegram_id),
    }


async def get_user_orders(telegram_id: int) -> list[dict]:
    """Foydalanuvchi buyurtmalarini backend API'dan olish."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_BASE_URL}/orders/",
                headers=_get_bot_headers(telegram_id),
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # DRF paginated yoki list
                    if isinstance(data, dict) and "results" in data:
                        return data["results"]
                    if isinstance(data, list):
                        return data
                return []
    except Exception as e:
        logger.error(f"Buyurtmalarni olishda xatolik: {e}")
        return []


def format_order_message(order: dict) -> str:
    """Buyurtmani formatlash."""
    status = STATUS_LABELS.get(order.get("status", ""), order.get("status", ""))
    payment = PAYMENT_LABELS.get(order.get("payment_method", ""), "")
    total = f"{int(float(order.get('total', 0))):,}".replace(",", " ")

    items = order.get("items", [])
    items_text = ""
    for item in items[:5]:
        product = item.get("product", {})
        name = product.get("name", "Noma'lum")
        qty = item.get("quantity", 1)
        price = f"{int(float(item.get('price', 0))):,}".replace(",", " ")
        items_text += f"  \u2022 {name} x{qty} \u2014 {price} so'm\n"

    if len(items) > 5:
        items_text += f"  ... va yana {len(items) - 5} ta\n"

    msg = (
        f"\U0001f6cd <b>Buyurtma #{order.get('id', 0):05d}</b>\n"
        f"\U0001f4cb Holat: {status}\n"
        f"\U0001f4b3 To'lov: {payment}\n"
    )

    if order.get("is_paid"):
        msg += "\u2705 To'langan\n"

    msg += f"\n\U0001f4e6 <b>Mahsulotlar:</b>\n{items_text}"
    msg += f"\n\U0001f4b0 <b>Jami: {total} so'm</b>"

    return msg


async def send_status_notification(
    bot, telegram_id: int, order: dict, new_status: str
) -> bool:
    """Buyurtma holati o'zgarganda foydalanuvchiga xabar yuborish."""
    status_label = STATUS_LABELS.get(new_status, new_status)
    order_id = order.get("id", 0)
    total = f"{int(float(order.get('total', 0))):,}".replace(",", " ")

    text = (
        f"\U0001f514 <b>Buyurtma yangilandi!</b>\n\n"
        f"\U0001f6cd Buyurtma: <b>#{order_id:05d}</b>\n"
        f"\U0001f4cb Yangi holat: <b>{status_label}</b>\n"
        f"\U0001f4b0 Summa: <b>{total} so'm</b>\n"
    )

    if new_status == "confirmed":
        text += "\n\u2705 Buyurtmangiz tasdiqlandi! Tez orada tayyorlaymiz."
    elif new_status == "processing":
        text += "\n\U0001f504 Buyurtmangiz tayyorlanmoqda..."
    elif new_status == "shipped":
        text += "\n\U0001f69a Buyurtmangiz yo'lga chiqdi!"
    elif new_status == "delivered":
        text += "\n\U0001f389 Buyurtmangiz yetkazildi! Xaridingiz uchun rahmat!"
    elif new_status == "cancelled":
        text += "\n\u274c Buyurtmangiz bekor qilindi. Savollar uchun bog'laning."

    try:
        await bot.send_message(chat_id=telegram_id, text=text, parse_mode="HTML")
        return True
    except Exception as e:
        logger.error(f"Xabar yuborishda xatolik (user {telegram_id}): {e}")
        return False
