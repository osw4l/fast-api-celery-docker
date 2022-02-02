import os
import time
import json
from celery import Celery
from ftplib import FTP
import datetime
from prometheus_client import Counter
from celery.schedules import crontab

celery = Celery(__name__)

celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND')
celery.conf.timezone = os.environ.get('TIMEZONE')

celery.conf['CELERY_ENABLE_UTC'] = False
celery.conf['CELERY_TIMEZONE'] = os.environ.get('TIMEZONE')
KAFKA_SERVER = os.environ.get('KAFKA_SERVER')

REQUEST_COUNT = Counter(
    "kafka_counter",
    "Count of kafka messages",
    ["source"]
)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*"),
        kafka_emitter.s(),
    )


@celery.task(name="task_test", trail=True)
def task_test():
    time.sleep(5)
    return {
        "result": True
    }


@celery.task(name="task_fail", trail=True)
def task_fail():
    raise Exception({
        "error": "test error by osw4l"
    })


@celery.task(name="periodic_done", trail=True)
def periodic_done():
    time.sleep(2)
    return {
        "result_periodic": True
    }


@celery.task(name="periodic_fail", trail=True)
def periodic_fail():
    raise Exception({
        "error": "periodic fail test error by osw4l"
    })


@celery.task(name="ftp_collector", trail=True)
def ftp_collector():
    ftp = FTP('ftp')
    ftp.login('globant', 'globant')
    ftp.cwd('/')
    files = ftp.nlst()

    for f in files:
        print(f, flush=True)

    files_to_add = [
        f'file_{f}'
        for f in range(50)
    ]

    for file in files_to_add:
        with open(f"{file}.json", "w") as f:
            f.write('{"h": true}')

        with open(f"{file}.json", "rb") as f:
            ftp.storbinary(f'STOR {file}.json', f)

        os.remove(f"{file}.json")

    ftp.quit()
    return {
        "file": True
    }


@celery.task(name="kafka_emitter", trail=True)
def kafka_emitter():
    REQUEST_COUNT.labels("kafka_emitter").inc()
    return {
        'message_sent': True
    }


if __name__ == '__main__':
    celery.worker_main()

