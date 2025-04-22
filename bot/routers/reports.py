import os
from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup
from dotenv import load_dotenv

from bot.db.connect_pg import get_repo
from bot.info.reports import report_type_text
from bot.repositories.logins import LoginsRepo
from bot.routers.main_menu import get_main_menu
from bot.routers.report_buttons.client_report import client_report_buttons
from bot.routers.report_buttons.daily_report import daily_report_buttons
from bot.routers.report_buttons.main import main_buttons
from bot.routers.report_buttons.report_by_login import create_login_report_menu
from bot.services.balance import get_balance_stat_from_yd
from bot.services.campaigns_stat import get_campaign_stat_from_yd
from bot.services.client_logins import get_logins_from_yd, login_handler
from bot.services.create_simple_report import get_simple_report_service

router = Router()
load_dotenv()
test_client = os.getenv('TEST_CLIENT')


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
async def client_report_menu(callback: types.CallbackQuery) -> None:
    await callback.message.edit_reply_markup(
        reply_markup=get_client_report_menu(),
    )
    await callback.answer()


@router.callback_query(F.data == "daily_report")
async def daily_report_menu(callback: types.CallbackQuery) -> None:
    await callback.message.edit_reply_markup(
        reply_markup=get_daily_report_menu(),
    )
    await callback.answer()


@router.callback_query(F.data == "login_report_menu_account")
async def login_report_menu_account(callback: types.CallbackQuery) -> None:
    cached_logins = await login_handler(callback)
    kb = InlineKeyboardMarkup(
        inline_keyboard=create_login_report_menu(cached_logins, True),
    )
    await callback.message.edit_reply_markup(
        reply_markup=kb,
    )
    await callback.answer()


@router.callback_query(F.data == "login_report_menu")
async def login_report_menu(callback: types.CallbackQuery) -> None:
    cached_logins = await login_handler(callback)
    kb = InlineKeyboardMarkup(
        inline_keyboard=create_login_report_menu(cached_logins),
    )
    await callback.message.edit_reply_markup(
        reply_markup=kb,
    )
    await callback.answer()


@router.callback_query(F.data == "about_reports")
async def daily_report_menu(callback: types.CallbackQuery) -> None:
    await callback.message.answer(
        text=report_type_text,
    )
    await callback.answer()


@router.callback_query(F.data == "get_logins")
async def get_client_logins(callback: types.CallbackQuery):
    logins = await get_logins_from_yd(callback)
    await callback.message.answer(
        text=f"Вы получили {len(logins)} клиентов"
    )
    async with get_repo(LoginsRepo) as repo:
        await repo.update_logins(logins_list=logins)
    await callback.answer()


@router.callback_query(F.data == "get_base")
async def get_client_campaigns(callback: types.CallbackQuery):
    campaigns = await get_campaign_stat_from_yd(callback, test_client)
    await callback.message.answer(
        text=f"Вы получили статистику за 5 дней"
    )
    await callback.answer()


@router.callback_query(F.data == "get_balance")
async def get_client_balance(callback: types.CallbackQuery):
    balance = await get_balance_stat_from_yd(callback, [test_client])
    await callback.message.answer(
        text=f"Вы получили баланс данные"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("get_simple_report"))
async def get_simple_report(callback: types.CallbackQuery):
    report_message = await get_simple_report_service(callback)
    await callback.message.answer(
        text=report_message,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("get_account_report"))
async def get_simple_report(callback: types.CallbackQuery):
    report_message = await get_simple_report_service(
        callback,
        rep_type='Account',
    )
    await callback.message.answer(
        text=report_message,
    )
    await callback.answer()
