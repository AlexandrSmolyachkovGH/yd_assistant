from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings
import redis.asyncio as redis

load_dotenv()


@dataclass
class BotData:
    chat_id: int | str
    access_token: Optional[str] = None

    def update_token(self, token: str | None):
        self.access_token = token


class BotSettings(BaseSettings):
    BOT_TOKEN: SecretStr
    BOT_URI: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


bot_data: Optional[BotData] = None
bot_settings = BotSettings()

redis_client = redis.Redis(
    host=bot_settings.REDIS_HOST,
    port=bot_settings.REDIS_PORT,
    password=bot_settings.REDIS_PASSWORD.get_secret_value(),
    decode_responses=True,
)
