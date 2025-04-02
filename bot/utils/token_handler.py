from redis.asyncio import Redis

from bot import config as c


class TokenHandler:
    inst: c.BotData = c.bot_data
    red: Redis = c.redis_client

    @property
    def chat_id(self) -> str:
        return str(self.inst.chat_id)

    async def set_token(self, token: str | None) -> None:
        self.inst.update_token(token=token)
        await self.red.set(
            name=self.chat_id,
            value=token,
        )

    async def get_token(self) -> str:
        token = self.inst.access_token
        if token is None:
            redis_token = await self.red.get(name=self.chat_id)
            if redis_token:
                token = redis_token.decode("utf-8")
                self.inst.update_token(token=token)
        return token if token else f"У вас нет активного токена."

    async def delete_token(self):
        self.inst.update_token(None)
        await self.red.delete(self.chat_id)


token_handler = TokenHandler()
