from bot.db.models import balance
from bot.repositories.base import BaseRepo
from sqlalchemy import select, insert, update, delete


class BalanceRepo(BaseRepo):

    @staticmethod
    def build_conditions_from_dict(table, filters: dict):
        return [table.c[key] == value for key, value in filters.items()]

    async def select_all(self):
        stmt = select(balance)
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def select(self, filter_args: dict):
        conditions = self.build_conditions_from_dict(balance, filter_args)
        stmt = (
            select(balance).
            where(*conditions)
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def insert(self, balance_records: list[dict]):
        stmt = (
            insert(balance)
            .returning(balance)
        )
        result = await self.session.execute(stmt, balance_records)
        await self.session.commit()
        return result.mappings().all()

    async def delete(self, filter_args: dict):
        conditions = self.build_conditions_from_dict(balance, filter_args)
        stmt = (
            delete(balance)
            .where(*conditions)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update(self, filter_args: dict, values: dict):
        conditions = self.build_conditions_from_dict(balance, filter_args)
        stmt = (
            update(balance)
            .where(*conditions)
            .values(**values)
            .returning(balance)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result

