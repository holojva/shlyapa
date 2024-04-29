from celery import shared_task
from celery.utils.log import get_task_logger
# from time import sleep

logger = get_task_logger(__name__)


@shared_task
def todo_notification(*args) :
    from maingame.views import test
    logger.info("initialized a notification for todo")
    print(args)
    test("axaxaxaxa")
    