import asyncio
from datetime import date
from aiogram import types

from bot.services.balance import get_balance_stat_from_yd
from bot.services.campaigns_stat import get_campaign_stat_from_yd
from bot.services.client_logins import get_logins_from_yd
from bot.services.login_stat import get_account_stat_from_yd


async def get_simple_report_service(
        callback: types.CallbackQuery,
        rep_type: str = 'Campaign',
        date_from: str = date.today().isoformat(),
        date_to: str = date.today().isoformat(),
) -> str:
    login_prefix = 'get_simple_report_' if rep_type == 'Campaign' else 'get_account_report_'
    login = callback.data.replace(login_prefix, '')

    login_stat, balance_stat, stat = await asyncio.gather(
        get_logins_from_yd(callback, login),
        get_balance_stat_from_yd(callback, [login]),
        get_campaign_stat_from_yd(callback, login, date_from, date_to) if rep_type == 'Campaign'
        else get_account_stat_from_yd(callback, login, date_from, date_to)
    )

    data = []
    for c in stat:
        common_row = (
            f"Показы: {c.get('impressions')}\n"
            f"Клики: {c.get('clicks')}\n"
            f"CTR, %: {round(c.get('clicks') / c.get('impressions') * 100, 2) if c.get('impressions') != 0 else 0}\n"
            f"CPC, RUB: {c.get('cost') / c.get('clicks') if c.get('clicks') != 0 else 0}\n"
            f"Клики: {c.get('cost')}\n"
            f"────────────────────\n"
        )
        if rep_type == "Campaign":
            common_row = f"📍 {c.get('campaign_name').upper()}\n" + common_row
        data.append(common_row)

    quality = login_stat[0]["quality"]
    quality_rec = ''
    if float(quality) < 6:
        quality_rec = ". Необходимо провести анализ и оптимизации"

    balance = round(balance_stat[0]["amount"] / 100, 2)
    day_limit = balance_stat[0]["daily_budget"] / 100
    balance_msg = ''
    if day_limit != 0:
        balance_remaining = int(balance / day_limit)
        balance_msg = f" Дней работы: {balance_remaining} (при текущих расходах)."
    else:
        day_limit = 'Не установлено'
    day_limit_str = str(day_limit) if isinstance(day_limit, (int, float)) else day_limit

    report_message = (
        f"🔹 Клиент: {str(login)};\n"
        f"🔹 Качество аккаунта: {quality}{quality_rec};\n"
        f"🔹 Активный бюджет: {str(balance)} руб;\n"
        f"🔹 Дневное ограничение аккаунта: {day_limit_str}.\n"
        f"🔹 {balance_msg}\n"
        f"────────────────────\n"
        f"Статистика по {['Аккаунту', 'РК'][rep_type == 'Campaign']}:\n"
        f"────────────────────\n"
        f"{''.join([row for row in data])}"
    )

    return report_message
