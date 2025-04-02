from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.routers.main_menu import get_main_menu

router = Router()


def get_reports_menu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Ежедневный отчет", callback_data="daily_report"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "reports")
async def report_menu(callback: types.CallbackQuery) -> None:
    await callback.message.edit_reply_markup(
        reply_markup=get_reports_menu(),
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: types.CallbackQuery) -> None:
    await callback.message.edit_reply_markup(
        reply_markup=get_main_menu(),
    )
    await callback.answer()
