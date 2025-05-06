from bot.services.background_tasks.celery_app import celery_app
from logger.background_tasks import background_logger

if __name__ == '__main__':
    background_logger.info("[run_worker.py] Celery worker начал работу")
    celery_app.worker_main([
        'worker',
        '--loglevel=debug',
        '--pool=solo',
        '-Q', 'report_queue'
    ])
