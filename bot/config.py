from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings
import redis.asyncio as redis

load_dotenv()


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


bot_settings = BotSettings()

redis_client = redis.Redis(
    host=bot_settings.REDIS_HOST,
    port=bot_settings.REDIS_PORT,
    password=bot_settings.REDIS_PASSWORD.get_secret_value(),
    decode_responses=True,
)
