from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards import get_main_keyboard, get_back_keyboard
from utils.api import get_user_orders, format_order_message

router = Router()


@router.callback_query(F.data == "my_orders")
async def cb_my_orders(callback: CallbackQuery):
    """Buyurtmalarim — API'dan olish"""
    telegram_id = callback.from_user.id
    orders = await get_user_orders(telegram_id)

    if not orders:
        await callback.message.edit_text(
            "📦 <b>Sizning buyurtmalaringiz</b>\n\n"
            "Hozircha buyurtmalar yo'q.\n"
            "Do'konni ochib, xarid qiling! 🛍",
            reply_markup=get_back_keyboard(),
        )
        await callback.answer()
        return

    text = f"📦 <b>Buyurtmalaringiz ({len(orders)} ta)</b>\n\n"

    for order in orders[:5]:
        text += format_order_message(order) + "\n\n"

    if len(orders) > 5:
        text += f"📋 Batafsil ko'rish uchun /orders buyrug'ini yuboring"

    await callback.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback.answer()


@router.callback_query(F.data == "contact")
async def cb_contact(callback: CallbackQuery):
    """Aloqa ma'lumotlari"""
    await callback.message.edit_text(
        "📞 <b>Biz bilan bog'lanish</b>\n\n"
        "📱 Telefon: +998 XX XXX XX XX\n"
        "📧 Email: info@jewelry.uz\n"
        "📍 Manzil: Toshkent sh., ...\n\n"
        "⏰ Ish vaqti: 09:00 - 21:00",
        reply_markup=get_back_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "help")
async def cb_help(callback: CallbackQuery):
    """Yordam"""
    await callback.message.edit_text(
        "ℹ️ <b>Yordam</b>\n\n"
        "🔹 <b>Qanday buyurtma beraman?</b>\n"
        "\"Do'konni ochish\" tugmasini bosing, mahsulotni tanlang va savatga qo'shing.\n\n"
        "🔹 <b>To'lov qanday?</b>\n"
        "💵 Naqd pul (yetkazib berishda)\n"
        "💳 Karta o'tkazma (oldindan)\n\n"
        "🔹 <b>Yetkazib berish</b>\n"
        "500,000 so'mdan yuqori — bepul!\n"
        "Qolganlar uchun 30,000 so'm.\n"
        "Toshkent bo'ylab 1-2 kun ichida.\n\n"
        "❓ Boshqa savollar uchun @admin_username ga yozing.",
        reply_markup=get_back_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_main")
async def cb_back_to_main(callback: CallbackQuery):
    """Asosiy menyuga qaytish"""
    await callback.message.edit_text(
        "✨ <b>JEWELRY</b> - premium zargarlik buyumlari\n\n"
        "Do'konimizni ochish uchun quyidagi tugmani bosing 👇",
        reply_markup=get_main_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lang_"))
async def cb_language(callback: CallbackQuery):
    """Til tanlash"""
    lang = callback.data.split("_")[1]
    lang_name = "O'zbekcha" if lang == "uz" else "Русский"
    await callback.answer(f"Til tanlandi: {lang_name}", show_alert=True)
