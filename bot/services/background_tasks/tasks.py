from celery import schedules
from celery.utils.log import get_task_logger

from bot.services.background_tasks.celery_app import celery_app
from bot.db.connect_pg import get_repo
from bot.repositories.logins import LoginsRepo
from bot.services.client_logins import get_logins_from_yd
from bot.config import bot_settings
from logger.background_tasks import background_logger

agency_token = bot_settings.AGENCY_TOKEN
task_logger = get_task_logger(__name__)


@celery_app.task
def test_print():
    task_logger.info("=== LOGGER TEST ===")
    background_logger.info("=== LOGGER TEST ===")
    print('_____TEST_____')


# @celery_app.task(queue='report_queue', bind=True, max_retries=3)
# async def update_client_list(self, admin_token=agency_token.get_secret_value()):
#     """Update client's information via admin account"""
#     print("FOO update_client_list WAS LAUNCHED")
#     # if not admin_token:
#     #     raise ValueError("Empty admin token value")
#     # logins = await get_logins_from_yd(admin_token=admin_token)
#     # try:
#     #     async with get_repo(LoginsRepo) as repo:
#     #         await repo.update_logins(logins)
#     # except Exception as e:
#     #     raise self.retry(exc=e, countdown=600)

#
# @celery_app.task(queue='report_queue', bind=True, max_retries=3)
# def update_reports(self, admin_token):
#     """Update the date for reports for the specified period"""
#     if not admin_token:
#         raise ValueError("Empty admin token value")
#     try:
#         ...
#     except Exception as e:
#         ...
#
#
# @celery_app.task(queue='report_queue', bind=True, max_retries=3)
# def prepare_reports(self, admin_token):
#     """Prepare reports for each client"""
#     if not admin_token:
#         raise ValueError("Empty admin token value")
#
#
# @celery_app.task(queue='report_queue', bind=True, max_retries=3)
# def send_reports(self, admin_token):
#     """Delivers reports to users with account access"""
#     if not admin_token:
#         raise ValueError("Empty admin token value")


celery_app.conf.broker_connection_retry_on_startup = True

celery_app.conf.beat_schedule = {
    "check_membership": {
        "task": 'test_print',
        "schedule": schedules.timedelta(seconds=5),
        # "schedule": schedules.crontab(hour='6', minute='0'),
    },
}
