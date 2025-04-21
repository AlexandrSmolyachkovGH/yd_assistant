from bot.db.models import campaigns_stat
from bot.repositories.base import BaseRepo
from sqlalchemy import select, insert, update, delete


class CampaignsRepo(BaseRepo):

    @staticmethod
    def build_conditions_from_dict(table, filters: dict):
        return [table.c[key] == value for key, value in filters.items()]

    async def select_all(self):
        stmt = select(campaigns_stat)
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def select(self, filter_args: dict):
        conditions = self.build_conditions_from_dict(campaigns_stat, filter_args)
        stmt = (
            select(campaigns_stat).
            where(*conditions)
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def insert(self, campaigns_list: list[dict]):
        stmt = (
            insert(campaigns_stat)
            .returning(campaigns_stat)
        )
        result = await self.session.execute(stmt, campaigns_list)
        await self.session.commit()
        return result.mappings().all()

    async def delete(self, filter_args: dict):
        conditions = self.build_conditions_from_dict(campaigns_stat, filter_args)
        stmt = (
            delete(campaigns_stat)
            .where(*conditions)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update(self, filter_args: dict, values: dict):
        conditions = self.build_conditions_from_dict(campaigns_stat, filter_args)
        stmt = (
            update(campaigns_stat)
            .where(*conditions)
            .values(**values)
            .returning(campaigns_stat)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.mappings().all()
