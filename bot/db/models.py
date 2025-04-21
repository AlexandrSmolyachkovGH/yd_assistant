from sqlalchemy import Column, Integer, String, DateTime, Table, MetaData, Enum, Date
import datetime
import enum

metadata_obj = MetaData()


class ArchiveStatusEnum(enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


logins = Table(
    "logins",
    metadata_obj,
    Column("id", Integer, primary_key=True, index=True),
    Column("client_id", Integer, nullable=False),
    Column("login", String, nullable=False, unique=True),
    Column("quality", String),
    Column("archive", Enum(
        ArchiveStatusEnum, name="archive_status_enum",
    ), default=ArchiveStatusEnum.ACTIVE),
    Column("update_date", DateTime, default=datetime.datetime.utcnow()),
)

campaigns_stat = Table(
    "campaigns_stat",
    metadata_obj,
    Column("id", Integer, primary_key=True, index=True),
    Column("date", Date, nullable=False),
    Column("login", String, nullable=False, unique=True),
    Column("campaign_name", String),
    Column("impressions", Integer),
    Column("clicks", Integer),
    Column("cost", Integer),  # cost / 10 000 -> (cents)
    Column("conversions", Integer),
)

balance = Table(
    'balance',
    metadata_obj,
    Column("id", Integer, primary_key=True, index=True),
    Column("login", String, nullable=False),
    Column("amount", Integer, nullable=False),  # amount * 100 -> (cents)
    Column("currency", String, nullable=False, default="RUB"),
    Column("daily_budge", Integer),
    Column("update_date", DateTime, default=datetime.datetime.utcnow()),
)
