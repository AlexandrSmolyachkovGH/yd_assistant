from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.routers.main_menu import get_main_menu

router = Router()


def get_settings_menu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Добавить клиента", callback_data="add_clients"),
            InlineKeyboardButton(text="Настроить рассылку", callback_data="config_auto_sending"),
        ],
        [
            InlineKeyboardButton(text="Справка", callback_data="settings_info"),
            InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "settings")
async def go_to_settings_menu(callback: types.CallbackQuery) -> None:
    await callback.message.edit_reply_markup(
        reply_markup=get_settings_menu(),
    )


@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=get_main_menu(),
    )
    await callback.answer()
