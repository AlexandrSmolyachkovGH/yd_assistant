from bot.db.models import logins
from bot.repositories.base import BaseRepo
from sqlalchemy import select, insert, update, delete


class LoginsRepo(BaseRepo):

    async def select_all(self):
        stmt = select(logins)
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def select(self, filter_arg):
        try:
            f = int(filter_arg)
            column = logins.c.client_id
            value = f
        except (ValueError, TypeError):
            column = logins.c.login
            value = filter_arg
        stmt = select(logins).where(column == value)
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def insert(self, logins_list: list[dict]):
        stmt = insert(logins).returning(logins)
        result = await self.session.execute(stmt, logins_list)
        await self.session.commit()
        return result.mappings().all()

    async def delete(self, *args, **kwargs):
        pass

    async def update(self, *args, **kwargs):
        pass
