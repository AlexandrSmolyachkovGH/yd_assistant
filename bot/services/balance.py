import httpx
from aiogram import types

from bot.config import bot_settings

from bot.routers.auth import get_token_foo


async def get_balance_stat_from_yd(
        callback: types.CallbackQuery,
        client_logins: list[str],
) -> dict:
    token = await get_token_foo(callback)
    if not token:
        print("Нет активного токена")
        raise

    params = {
        "Action": "Get",
        "SelectionCriteria": {
            "Logins": client_logins,
        },
    }

    body = {
        "method": "AccountManagement",
        "token": token,
        "locale": "ru",
        "param": params,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                bot_settings.CLIENT_BALANCE_URI,
                json=body,
            )
            response.raise_for_status()
            data = response.json()['data']['Accounts']
            result = [
                {
                    "login": x['Login'],
                    "amount": x['Amount'],
                    "daily_budget": x['AccountDayBudget'],
                    "currency": x['Currency'],
                } for x in data
            ]
            return result
    except httpx.HTTPStatusError as e:
        print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        raise
