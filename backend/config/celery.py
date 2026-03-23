import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("jewelry_shop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "sync-bts-tracking-every-2-hours": {
        "task": "apps.delivery.tasks.sync_bts_tracking",
        "schedule": crontab(minute=0, hour="*/2"),
    },
}
