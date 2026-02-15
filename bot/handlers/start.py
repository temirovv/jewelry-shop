from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from keyboards import get_main_keyboard
from utils.api import get_user_orders, format_order_message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Start buyrug'i"""
    await message.answer(
        f"✨ <b>Assalomu alaykum, {message.from_user.first_name}!</b>\n\n"
        "🏆 <b>JEWELRY</b> - premium zargarlik buyumlari do'koniga xush kelibsiz!\n\n"
        "Bizda:\n"
        "💎 Eng sifatli zargarlik buyumlari\n"
        "🏷 O'rikzor narxlari\n"
        "🎁 Premium qadoqlash\n"
        "🚚 Tez yetkazib berish\n\n"
        "Do'konimizni ochish uchun quyidagi tugmani bosing 👇",
        reply_markup=get_main_keyboard(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Yordam buyrug'i"""
    await message.answer(
        "ℹ️ <b>Yordam</b>\n\n"
        "🔹 /start - Botni qayta ishga tushirish\n"
        "🔹 /help - Yordam\n"
        "🔹 /orders - Buyurtmalarim\n\n"
        "🔹 <b>Qanday buyurtma beraman?</b>\n"
        "\"Do'konni ochish\" tugmasini bosing, mahsulotni tanlang, "
        "savatga qo'shing va checkout sahifasida buyurtmani rasmiylang.\n\n"
        "🔹 <b>To'lov usullari:</b>\n"
        "💵 Naqd pul (yetkazib berishda)\n"
        "💳 Karta o'tkazma (oldindan)\n\n"
        "🔹 <b>Yetkazib berish:</b>\n"
        "500,000 so'mdan yuqori buyurtmalarga bepul!\n"
        "Qolganlar uchun 30,000 so'm.\n\n"
        "❓ Savollaringiz bo'lsa, @admin_username ga yozing.",
    )


@router.message(Command("orders"))
async def cmd_orders(message: Message):
    """Buyurtmalar ro'yxati — API'dan olish"""
    telegram_id = message.from_user.id
    orders = await get_user_orders(telegram_id)

    if not orders:
        await message.answer(
            "📦 <b>Buyurtmalaringiz</b>\n\n"
            "Hozircha buyurtmalar yo'q.\n"
            "Do'konni ochib, birinchi xaridingizni qiling! 🛍",
            reply_markup=get_main_keyboard(),
        )
        return

    text = f"📦 <b>Sizning buyurtmalaringiz ({len(orders)} ta)</b>\n\n"

    for order in orders[:10]:
        text += format_order_message(order) + "\n\n" + "─" * 30 + "\n\n"

    if len(orders) > 10:
        text += f"... va yana {len(orders) - 10} ta buyurtma\n"

    text += "Batafsil ma'lumot uchun WebApp'ni oching 👇"

    await message.answer(text, reply_markup=get_main_keyboard())
