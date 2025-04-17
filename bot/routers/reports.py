from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup

from bot.routers.main_menu import get_main_menu
from bot.routers.report_buttons.client_report import client_report_buttons
from bot.routers.report_buttons.daily_report import daily_report_buttons
from bot.routers.report_buttons.main import main_buttons
from bot.services.client_logins import get_logins_from_yd

router = Router()


def get_reports_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=main_buttons)


def get_client_report_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=client_report_buttons)


def get_daily_report_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=daily_report_buttons)


@router.callback_query(F.data.in_({"reports", "back_to_report_menu"}))
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


@router.callback_query(F.data == "client_report")
async def report_menu(callback: types.CallbackQuery) -> None:
    await callback.message.edit_reply_markup(
        reply_markup=get_client_report_menu(),
    )
    await callback.answer()


@router.callback_query(F.data == "daily_report")
async def report_menu(callback: types.CallbackQuery) -> None:
    await callback.message.edit_reply_markup(
        reply_markup=get_daily_report_menu(),
    )
    await callback.answer()


@router.callback_query(F.data == "get_logins")
async def report_menu(callback: types.CallbackQuery) -> None:
    logins = await get_logins_from_yd(callback)
    await callback.message.answer(
        text=f"Вы получили {len(logins)} клиентов"
    )
    await callback.answer()
