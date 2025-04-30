from bot.services.background_tasks.celery_app import celery_app

if __name__ == '__main__':
    celery_app.worker_main([
        'worker',
        '--loglevel=info',
        '--pool=solo',
        '-Q', 'report_queue'
    ])
