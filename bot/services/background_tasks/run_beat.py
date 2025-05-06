from bot.services.background_tasks.celery_app import celery_app
from logger.background_tasks import background_logger

if __name__ == "__main__":
    background_logger.info("[run_beat.py] Celery beat начал работу")
    celery_app.start(
        argv=['beat', '--loglevel=info'],
    )
