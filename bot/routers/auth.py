from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.routers.main_menu import get_main_menu
from bot.config import redis_client, bot_data
from bot.utils.token_handler import token_handler
from yandex_auth.config import auth_settings as conf

router = Router()


async def get_auth_menu(telegram_chat_id: int) -> InlineKeyboardMarkup:
    token = await token_handler.get_token()
    if token:
        print(token)
        get_token_btn = InlineKeyboardButton(
            text="Получить токен",
            callback_data="token_exists",
        )
    else:
        auth_url = conf.auth_dsn + f"&state={telegram_chat_id}"
        get_token_btn = InlineKeyboardButton(
            text="Получить токен",
            url=auth_url,
        )
    buttons = [
        [
            get_token_btn,
        ],
        [
            InlineKeyboardButton(text="Проверить токен", callback_data="check_auth_info"),
            InlineKeyboardButton(text="Удалить токен", callback_data="check_auth_info"),
        ],
        [
            InlineKeyboardButton(text="Справка", callback_data="auth_info"),
            InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "auth")
async def go_to_auth_menu(callback: types.CallbackQuery) -> None:
    telegram_chat_id = bot_data.chat_id
    keyboard = await get_auth_menu(telegram_chat_id)
    await callback.message.edit_reply_markup(
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data == "token_exists")
async def token_already_exists(callback: types.CallbackQuery) -> None:
    await callback.answer(
        text="У вас уже есть активный токен.",
        show_alert=True,
    )


@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: types.CallbackQuery) -> None:
    await callback.message.edit_reply_markup(
        reply_markup=get_main_menu(),
    )
    await callback.answer()
