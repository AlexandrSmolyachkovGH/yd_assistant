import httpx
from aiogram import types

from bot.config import bot_settings, redis_client
from bot.routers.auth import get_token_foo


async def get_logins_from_yd(
        callback: types.CallbackQuery | None = None,
        login: str = None,
        admin_token: str | None = None
) -> list[dict]:
    if admin_token:
        token = admin_token
    if callback:
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
    if login:
        agency_clients_body["params"]["SelectionCriteria"]["Logins"] = [login]
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


async def get_logins_from_cache(callback: types.CallbackQuery) -> list[str]:
    chat_id = callback.message.chat.id
    cached_logins = await redis_client.get(f"logins_{chat_id}")
    if cached_logins:
        return cached_logins.split(",")
    return []


async def put_logins_in_cache(callback: types.CallbackQuery, logins: list[str]) -> None:
    chat_id = callback.message.chat.id
    logins_str = ",".join(logins)
    await redis_client.set(
        name=f"logins_{chat_id}",
        value=logins_str,
    )


async def login_handler(callback: types.CallbackQuery) -> list[str]:
    cached_logins = await get_logins_from_cache(callback)
    if not cached_logins:
        logins = await get_logins_from_yd(callback)
        cached_logins = [elem['login'] for elem in logins]
        await put_logins_in_cache(callback, cached_logins)
    return cached_logins
