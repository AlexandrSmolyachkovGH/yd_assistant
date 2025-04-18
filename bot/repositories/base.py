from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepo(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def select(self, *args, **kwargs):
        pass

    @abstractmethod
    async def insert(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs):
        pass

    @abstractmethod
    async def update(self, *args, **kwargs):
        pass
