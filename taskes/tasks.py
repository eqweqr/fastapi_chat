from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timezone, timedelta
# from customlog import custom_logger
# from customlog.logger import logger1
from taskes.__init__ import redis_chats 
import time
from service.email_confirm import create_msg, send_msg


app = Celery('tasks', broker='amqp://leo:password@localhost:5672//')
app.conf.result_backend = 'redis://localhost:6379'

@app.task
def send_confimation_message(email):
    msg = create_msg(email)
    send_msg(msg, email)


    
@app.task
def delete_expired_message(chat_id):
    now = datetime.now(timezone.utc)
    delta = timedelta(days=1)
    val=(now-delta).timestamp()
    expired_messages = redis_chats.zremrangebyscore('chat_'+chat_id, min=0, max=val)


app.conf.beat_schedule = {
    "run-me-every-ten-seconds": {
    "task": "tasks.delete_expired_message",
    "schedule": crontab(minute=0, hour=15),
    }
}