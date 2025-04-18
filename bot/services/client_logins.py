import httpx
from aiogram import types

from bot.config import bot_settings
from bot.routers.auth import get_token_foo


async def get_logins_from_yd(callback: types.CallbackQuery):
    token = await get_token_foo(callback)
    if not token:
        print("Нет активного токена")
        raise
    uri = bot_settings.CLIENT_LOGINS_URI
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept-Language": "ru",
        "Content-Type": "application/json",
    }
    agency_clients_body = {
        "method": "get",
        "params": {
            "SelectionCriteria": {
                "Archived": "NO",
            },
            "FieldNames": ["Login", "ClientId", "AccountQuality"],
        }
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                uri,
                headers=headers,
                json=agency_clients_body,
            )
            response.raise_for_status()
            data = response.json()["result"]["Clients"]
            parsed_data = [
                {
                    'client_id': d['ClientId'],
                    'login': d['Login'],
                    'quality': str(d['AccountQuality']),

                }
                for d in data
            ]
            return parsed_data
    except httpx.HTTPStatusError as e:
        print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        raise
