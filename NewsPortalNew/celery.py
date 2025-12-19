import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Расписание задач (если не используешь CELERY_TASK_ALWAYS_EAGER = True)
app.conf.beat_schedule = {
    'send-weekly-digest': {
        'task': 'news.tasks.send_weekly_digest',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),  # Понедельник 9:00
    },
}
app.conf.timezone = 'Europe/Moscow'