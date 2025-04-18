from datetime import date, timedelta

import httpx
from aiogram import types

from bot.config import bot_settings
from bot.routers.auth import get_token_foo


async def get_campaign_stat_from_yd(
        callback: types.CallbackQuery,
        client_login: str,
        date_from: str | date = (date.today() - timedelta(days=5)).isoformat(),
        date_to: str | date = (date.today() - timedelta(days=1)).isoformat(),
):
    token = await get_token_foo(callback)
    if not token:
        print("Нет активного токена")
        raise
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Login": client_login,
        "Accept-Language": "ru",
        "Content-Type": "application/json",
    }
    agency_clients_body = {
        "method": "get",
        "params": {
            "SelectionCriteria": {
                "DateFrom": date_from,
                "DateTo": date_to,
            },
            "FieldNames": [
                "Date",
                "ClientLogin",
                "CampaignName",
                "Impressions",
                "Clicks",
                "Cost",
                "Conversions",
            ],
            "OrderBy": [{
                "Field": "Date",
            }],
            "ReportName": f"ACCOUNT {client_login}",
            "ReportType": "CAMPAIGN_PERFORMANCE_REPORT",
            "DateRangeType": "CUSTOM_DATE",
            "Format": "TSV",
            "IncludeVAT": "NO",
            "IncludeDiscount": "NO",
        }
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                bot_settings.CLIENT_REPORTS_URI,
                headers=headers,
                json=agency_clients_body,
            )
            response.raise_for_status()
            data = response.text.split('\n')[1:-1]
            result = [d.split('\t') for d in data]
            return result
    except httpx.HTTPStatusError as e:
        print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        raise
