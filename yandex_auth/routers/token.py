import httpx
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from aiogram import Bot

from yandex_auth.config import auth_settings as conf
from bot.config import bot_settings as bot_conf, redis_client

router = APIRouter()
bot = Bot(token=bot_conf.BOT_TOKEN.get_secret_value())


@router.get("/oauth/callback", tags=["TokenHandler"])
async def yandex_callback(request: Request):
    code = request.query_params.get('code')
    state = request.query_params.get('state')
    if not code:
        return {"error": "No code provided"}
    token_url = conf.ya_token_url
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": conf.CLIENT_ID.get_secret_value(),
        "client_secret": conf.CLIENT_SECRET.get_secret_value(),
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)

    token_info = response.json()
    access_token = token_info.get("access_token")

    if access_token:
        await redis_client.set(state, access_token)
        await bot.send_message(
            chat_id=state,
            text=f"✅ Ваш токен успешно получен!\n"
                 f"🔑 Access token:\n"
                 f"{access_token[:6]}****{access_token[-6:]}"
        )
        return RedirectResponse(url=bot_conf.BOT_URI)
    else:
        return {"error": "Access token not found"}
