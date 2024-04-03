from taskes.white_list import DenyList
from redis import StrictRedis

redis_message = DenyList('localhost', 6379)
redis_chats = StrictRedis('localhost', 6379)