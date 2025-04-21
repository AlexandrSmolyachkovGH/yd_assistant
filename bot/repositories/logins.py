from datetime import datetime

from bot.db.models import logins, ArchiveStatusEnum
from bot.repositories.base import BaseRepo
from sqlalchemy import select, insert, update, delete


class LoginsRepo(BaseRepo):

    @staticmethod
    def select_filter_arg(filter_value):
        try:
            f = int(filter_value)
            column = logins.c.client_id
            value = f
        except (ValueError, TypeError):
            column = logins.c.login
            value = filter_value
        return column, value

    async def select_all(self):
        stmt = select(logins)
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def select_logins(self):
        stmt = select(logins.c.login)
        result = await self.session.execute(stmt)
        return result.fetchall()

    async def select(self, filter_arg):
        column, value = self.select_filter_arg(filter_value=filter_arg)
        stmt = select(logins).where(column == value)
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def insert(self, logins_list: list[dict]):
        stmt = insert(logins).returning(logins)
        result = await self.session.execute(stmt, logins_list)
        await self.session.commit()
        return result.mappings().all()

    async def delete(self, filter_arg: int | str):
        column, value = self.select_filter_arg(filter_value=filter_arg)
        stmt = delete(logins).where(column == value)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update(self, filter_arg: int | str, values: dict):
        column, value = self.select_filter_arg(filter_value=filter_arg)
        stmt = update(logins).where(column == value).values(**values).returning(logins)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result

    async def update_logins(self, new_logins):
        saved_logins = await self.select_all()

        saved_logins_set = {login['client_id'] for login in saved_logins}
        new_logins_set = {login['client_id'] for login in new_logins}

        archive_ids_set = saved_logins_set - new_logins_set
        update_ids_set = saved_logins_set & new_logins_set
        insert_ids_set = new_logins_set - saved_logins_set
        time_of_update = datetime.utcnow()
        new_logins_dict = {login['client_id']: login for login in new_logins}

        for login in saved_logins:
            if login['client_id'] in archive_ids_set:
                stmt = (
                    update(logins)
                    .where(logins.c.client_id == login['client_id'])
                    .values(
                        archive=ArchiveStatusEnum.ARCHIVED,
                        update_date=time_of_update,
                    )
                )
                await self.session.execute(stmt)

            elif login['client_id'] in update_ids_set:
                new_login = new_logins_dict.get(login['client_id'])
                stmt = (
                    update(logins)
                    .where(logins.c.client_id == login['client_id'])
                    .values(
                        update_date=time_of_update,
                        quality=new_login['quality'],
                    )
                )
                await self.session.execute(stmt)

        data_to_insert = [
            {**el, "update_date": time_of_update}
            for el in new_logins if el['client_id'] in insert_ids_set
        ]
        if data_to_insert:
            stmt = insert(logins).values(data_to_insert)
            await self.session.execute(stmt)

        await self.session.commit()
