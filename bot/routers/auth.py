from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

from bot.routers.main_menu import get_main_menu
from bot.config import redis_client
from yandex_auth.config import auth_settings as conf

router = Router()
temp_token = os.getenv("TEMP_TOKEN")


async def get_auth_menu(telegram_chat_id: int) -> InlineKeyboardMarkup:
    token = await redis_client.get(telegram_chat_id)
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
            InlineKeyboardButton(text="Проверить токен", callback_data="check_auth"),
            InlineKeyboardButton(text="Удалить токен", callback_data="delete_token"),
        ],
        [
            InlineKeyboardButton(text="Справка", callback_data="auth_info"),
            InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "auth")
async def go_to_auth_menu(callback: types.CallbackQuery) -> None:
    telegram_chat_id = callback.message.chat.id
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


async def get_token_foo(callback: types.CallbackQuery) -> str:
    token = await redis_client.get(callback.message.chat.id)
    return token


async def check_token_foo(callback: types.CallbackQuery) -> str:
    token = await redis_client.get(callback.message.chat.id)
    if not token:
        # мокаем тестовый токен
        await redis_client.set(
            name=callback.message.chat.id,
            value=temp_token,
        )
        # ----------------------
        msg = "У вас нет активного токена"
    else:
        # мокаем тестовый токен
        test_token = await redis_client.set(
            name=callback.message.chat.id,
            value=temp_token,
        )
        # ----------------------
        msg = "У вас есть активный токен:\n" \
              f"{token[:6]}****{token[-6:]}"

    return msg


@router.callback_query(F.data == "check_auth")
async def check_token(callback: types.CallbackQuery) -> None:
    msg = await check_token_foo(callback)
    await callback.message.answer(
        text=msg,
    )
    await callback.answer()


@router.callback_query(F.data == "delete_token")
async def delete_token(callback: types.CallbackQuery) -> None:
    await redis_client.delete(str(callback.message.chat.id))
    await callback.message.answer(
        text="Ваш токен был удален.\n" \
             f"Для доступа к сервисам получите новый токен",
    )
    await callback.answer()


@router.callback_query(F.data == "auth_info")
async def get_token_info(callback: types.CallbackQuery) -> None:
    with open(
            file="bot/info/auth.txt",
            mode="r",
            encoding='utf-8',
    ) as file:
        text = file.read()
    await callback.message.answer(
        text=text,
    )
    await callback.answer()
