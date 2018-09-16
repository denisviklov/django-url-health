import subprocess
import os

from celery.decorators import periodic_task, task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
BOT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'static/js/bot.js')

@task(ignore_result=True)
def scan_links(domain):
    from url_health.models import Scanning

    scan = Scanning.objects.first()

    #very first run let's create initial scan obj
    if scan == None:
        scan = Scanning.objects.create()

    if scan.status == Scanning.RUN:
        return

    scan.status = 1
    scan.save()

    logger.info('start scanning')

    try:
        subprocess.check_call(['casperjs', BOT_ROOT, domain])
    except:
        logger.info('scanning error')
    finally:
        scan.status = 0
        scan.save()
        logger.info('stop scanning')