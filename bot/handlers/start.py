from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from keyboards import get_main_keyboard

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
        parse_mode="HTML",
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Yordam buyrug'i"""
    await message.answer(
        "ℹ️ <b>Yordam</b>\n\n"
        "🔹 /start - Botni qayta ishga tushirish\n"
        "🔹 /help - Yordam\n"
        "🔹 /orders - Buyurtmalarim\n\n"
        "❓ Savollaringiz bo'lsa, @admin_username ga yozing.",
        parse_mode="HTML",
    )


@router.message(Command("orders"))
async def cmd_orders(message: Message):
    """Buyurtmalar ro'yxati"""
    await message.answer(
        "📦 <b>Sizning buyurtmalaringiz</b>\n\n"
        "Buyurtmalaringizni WebApp orqali ko'rishingiz mumkin.",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML",
    )
