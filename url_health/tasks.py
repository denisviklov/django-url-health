import subprocess
import os

from celery.decorators import periodic_task, task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
BOT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'static/js/bot.js')

@task(ignore_result=True)
def scan_links(domain):
    logger.info('start scanning')
    try:
        subprocess.check_call(['casperjs', BOT_ROOT, domain])
    except:
        logger.info('scanning error')
    finally:
        scan.status = 0
        scan.save()
        logger.info('stop scanning')