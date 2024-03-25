from celery import Celery
from celery.schedules import crontab


app = Celery('tasks', broker='amqp://@localhost:5672//')


app.conf.beat_schedule = {
    "run-me-every-ten-seconds": {
    "task": "service.message_cacher.add_message",
    "schedule": 10.0,
    "args": "fads",
    }
}