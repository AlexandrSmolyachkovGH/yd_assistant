from sqlalchemy import Column, Integer, String, Float, DateTime, Table, MetaData, Enum
import datetime
import enum

metadata_obj = MetaData()


class ArchiveStatusEnum(enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


logins = Table(
    'logins',
    metadata_obj,
    Column("id", Integer, primary_key=True, index=True),
    Column("client_id", Integer, nullable=False),
    Column("login", String, nullable=False, unique=True),
    Column("quality", String),
    Column("archive", Enum(
        ArchiveStatusEnum, name="archive_status_enum",
    ), default=ArchiveStatusEnum.ACTIVE),
)
