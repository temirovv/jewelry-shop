from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import WEBAPP_URL


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Asosiy klaviatura - WebApp ochish"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛍 Do'konni ochish",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ],
            [
                InlineKeyboardButton(
                    text="📦 Buyurtmalarim",
                    callback_data="my_orders",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📞 Aloqa",
                    callback_data="contact",
                ),
                InlineKeyboardButton(
                    text="ℹ️ Yordam",
                    callback_data="help",
                ),
            ],
        ]
    )


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Til tanlash klaviaturasi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            ]
        ]
    )


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Orqaga qaytish"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main"),
            ]
        ]
    )
