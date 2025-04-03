from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from bot.config import redis_client

from bot import config

router = Router()


def get_main_menu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Отчеты", callback_data="reports"),
            InlineKeyboardButton(text="Авторизация", callback_data="auth"),
        ],
        [
            InlineKeyboardButton(text="Настройки", callback_data="settings"),
            InlineKeyboardButton(text="Справка", callback_data="info"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command('start'))
async def start_bot(message: types.Message) -> None:
    await message.answer(
        text="👋 Добро пожаловать в Ассистент ЯндексДиректа!\n" \
             "Тут можно удобно:\n" \
             "🔹 Контролировать расходы рекламных аккаунтов;\n" \
             "🔹 Получать ежедневную статистику;\n" \
             "🔹 Отлавливать существенные изменения кампаний;\n" \
             "🔹 И все это в автоматическом режиме! 🚀",
        reply_markup=get_main_menu(),
    )


@router.message(Command('call_menu'))
async def call_menu(message: types.Message) -> None:
    await message.answer(
        text="Вы вызвали меню бота:",
        reply_markup=get_main_menu(),
    )


@router.message(Command('check_auth'))
async def check_auth(message: types.Message) -> None:
    token = await redis_client.get(message.chat.id)
    msg = "У вас есть активный токен"
    if not token:
        msg = "У вас нет токена"
    await message.answer(
        text=f"Проверка авторизации:\n"
             f"{msg}",
    )


@router.message(Command('ping'))
async def check_app(message: types.Message) -> None:
    await message.answer(
        text='pong',
    )
