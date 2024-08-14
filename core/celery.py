# yapf: disable
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# set the default Django settings module for the 'celery' program.

app = Celery('article_project', namespace='CELERY')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


def mins_to_seconds(mins):
    return mins * 60


tasks = {
    'celery_batch_update_article_ratings': {
        'task': 'article.tasks.batch_update_article_ratings',
        'schedule': mins_to_seconds(1),
    },
    'celery_update_stale_articles': {
        'task': 'article.tasks.update_stale_articles',
        'schedule': crontab(hour='23', minute='59'),
    },
    'celery_find_suspicious_ratings': {
        'task': 'article.tasks.find_suspicious_ratings',
        'schedule': mins_to_seconds(20),
    },
    'celery_flag_suspicious_articles': {
        'task': 'article.tasks.flag_suspicious_articles',
        'schedule': mins_to_seconds(60),
    },
}

app.conf.beat_schedule = tasks
