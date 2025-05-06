from celery import Celery
from bot.config import bot_settings

celery_app = Celery(
    'get_reports',
    broker=bot_settings.get_report_rabbit_dsn,
    backend=None,
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    worker_pool='asyncio',
    worker_hijack_root_logger=False,
)
