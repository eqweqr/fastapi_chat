from datetime import datetime, timezone, timedelta
from redis_access import redis_message
from customlog import logger
from tasks.tasks import app
from typing import List


list_chats: List[str] = []


def create_new_chat(chat_name: str) -> None:
    try:
        redis_message.zdd(chat_name, {'Chat Inited': datetime.now().timestamp()})
    except Exception as ex:
        logger.exception(ex)
    else:
        list_chats.append(chat_name)
        logger.info("chat created successfuly")


def add_message(chat_name: str, message: str) -> None:
    try:
        redis_message.zadd(chat_name, {message: datetime.now().timestamp()})
    except Exception as ex:
        logger.exception(ex)
    else:
        logger.info("message added successfuly")


@app.task
def delete_expired_message(chat_name: str):

    now = datetime.now(timezone.utc)
    delta = timedelta(seconds=15)
    val=(now-delta).timestamp()

    
    for chat in list_chats:
        expired_messages = redis_message.zrangebyscore(chat_name, min=0, max=val)
        for message in expired_messages:
            redis_message.zrem(chat, message)
        logger.info(len(expired_messages), 'was deleted from redis cache of', chat )