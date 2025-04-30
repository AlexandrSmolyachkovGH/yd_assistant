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
    CLIENT_LOGINS_URI: str
    CLIENT_REPORTS_URI: str
    CLIENT_BALANCE_URI: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: SecretStr
    RABBITMQ_DEFAULT_VHOST: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    AGENCY_TOKEN: SecretStr

    @property
    def get_postgres_uri(self) -> str:
        postgres_uri = (f"postgresql+asyncpg://"
                        f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@{self.POSTGRES_HOST}:"
                        f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}")
        return postgres_uri

    @property
    def get_report_rabbit_dsn(self) -> str:
        return f"amqp://" \
               f"{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS.get_secret_value()}@" \
               f"{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_DEFAULT_VHOST}"

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
