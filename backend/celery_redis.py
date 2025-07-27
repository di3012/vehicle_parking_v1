from celery import Celery
from celery.schedules import crontab
from config import devConfig

celery = Celery(__name__, broker=devConfig.CELERY_BROKER_URL, backend=devConfig.CELERY_RESULT_BACKEND)
celery.conf.update(devConfig.__dict__)

# Schedule for daily reminder at 6 PM (18:00)
celery.conf.beat_schedule = {
    'daily-parking-reminder': {
        'task': 'tasks.reminders.send_daily_reminder',
        'schedule': crontab(hour=18, minute=0),  # 🕕 6 PM every day
    },
}
celery.conf.timezone = 'Asia/Kolkata'
