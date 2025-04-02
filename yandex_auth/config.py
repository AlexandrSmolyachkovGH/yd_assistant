import webbrowser

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings

load_dotenv()


class YandexAPIAuth(BaseSettings):
    CLIENT_ID: SecretStr
    REDIRECT_URI: SecretStr
    CLIENT_SECRET: SecretStr
    TOKEN_URL: str

    @property
    def auth_dsn(self) -> str:
        return f"https://oauth.yandex.ru/authorize?response_type=code" \
               f"&client_id={self.CLIENT_ID.get_secret_value()}" \
               f"&redirect_uri={self.REDIRECT_URI.get_secret_value()}"

    @property
    def ya_token_url(self):
        return self.TOKEN_URL

    def open_auth_url(self) -> None:
        print("Перейди по ссылке для авторизации:")
        print(self.auth_dsn)
        webbrowser.open(self.auth_dsn)

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "allow"


auth_settings = YandexAPIAuth()
