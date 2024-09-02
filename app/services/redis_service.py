import redis
import os

redis_client = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), decode_responses=True)

def cache_message(session_id, message):
    redis_client.set(session_id, message)

def get_cached_message(session_id):
    return redis_client.get(session_id)
