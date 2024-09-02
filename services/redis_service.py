import redis
import json
import os

def get_redis_client():
    return redis.Redis.from_url(os.getenv("REDIS_URL"))

def cache_chat(session_id, messages):
    client = get_redis_client()
    client.set(session_id, json.dumps(messages))

def get_chat_from_cache(session_id):
    client = get_redis_client()
    chat = client.get(session_id)
    return json.loads(chat) if chat else []

def delete_chat_from_cache(session_id):
    client = get_redis_client()
    client.delete(session_id)

def update_message_in_cache(session_id, message_id, new_message):
    chat = get_chat_from_cache(session_id)
    for msg in chat:
        if msg['id'] == message_id:
            msg['message'] = new_message
            break
    cache_chat(session_id, chat)
