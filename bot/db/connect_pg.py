from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from bot.config import bot_settings

postgres_url = bot_settings.get_postgres_uri
async_engine = create_async_engine(
    url=postgres_url,
    echo=True,
    pool_size=10,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def get_repo(repo_class):
    async with AsyncSessionLocal() as session:
        yield repo_class(session)
