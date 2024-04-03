from datetime import datetime, timezone, timedelta
from customlog import custom_logger
from typing import List
from taskes.__init__ import redis_chats


def create_new_chat(chat_name: int) -> None:
    try:
        redis_chats.zadd('chat_'+chat_name, {'Chat Inited': datetime.now().timestamp()})
    except Exception as ex:
        custom_logger.exception(ex)
    else:
        custom_logger.info("chat created successfuly")


def add_message(chat_name: int, message: str, author: str) -> None:
    message_in_set = "zxcqwe".join([author, message])
    try:
        redis_chats.zadd('chat_'+chat_name, {message_in_set: datetime.now().timestamp()})
    except Exception as ex:
        custom_logger.exception(ex)
    else:
        custom_logger.info("message added successfuly")


def get_cached_messages(chat_name: int):
    cached_messages = redis_chats.zrange('chat_'+chat_name, 0, -1)
    return cached_messages
