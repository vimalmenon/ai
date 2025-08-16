from logging import getLogger

from tasks import celery_app

logger = getLogger(__name__)


@celery_app.task
def run_every_2_minutes():
    logger.warning("Task is running every 2 minutes")
