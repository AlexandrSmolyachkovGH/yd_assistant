from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.routers.main_menu import get_main_menu

router = Router()


def get_info_menu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Начать пользоваться", callback_data='how_to_start'),
            InlineKeyboardButton(text="Возможности бота", callback_data='bot_features'),
        ],
        [
            InlineKeyboardButton(text="Список команд", callback_data='list_of_commands'),
            InlineKeyboardButton(text="Назад", callback_data='back_to_main_menu'),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "info")
async def start_bot(callback: types.CallbackQuery) -> None:
    await callback.message.edit_reply_markup(
        reply_markup=get_info_menu(),
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: types.CallbackQuery) -> None:
    await callback.message.edit_reply_markup(
        reply_markup=get_main_menu(),
    )
    await callback.answer()
