# Import necessary modules
import redis  # Redis client library
import json   # Library for handling JSON data
import os     # Library for accessing environment variables

def get_redis_client():
    # Initialize and return a Redis client using the URL from the environment variable 'REDIS_URL'.
    return redis.Redis.from_url(os.getenv("REDIS_URL"))

def cache_chat(session_id, messages):
    # Cache chat messages for a specific session ID in Redis.
    
    # Args:
    #     session_id (str): The unique identifier for the chat session.
    #     messages (list): List of chat messages to be cached.
    client = get_redis_client()  # Get Redis client instance
    client.set(session_id, json.dumps(messages))  # Store messages as a JSON string in Redis

def cache_suggestions(message, data):
    # Cache suggestions associated with a specific message in Redis.
    
    # Args:
    #     message (str): The message for which suggestions are being cached.
    #     data (dict): The suggestions data to be cached.
    client = get_redis_client()  # Get Redis client instance
    client.set(f'suggestion-{message}', json.dumps(data))  # Store suggestions as a JSON string in Redis with a key prefix

def get_message_from_cache(message):
    # Retrieve cached suggestions for a specific message from Redis. If not found, retrieve standard suggestions.
    
    # Args:
    #     message (str): The message to look up in the cache.
    
    # Returns:
    #     list: The suggestions data as a list. If no data is found, returns an empty list.
    client = get_redis_client()  # Get Redis client instance
    key = f'suggestion-{message}'  # Generate the key for the specific message
    print("Key we are searching:", key)  # Log the key being searched

    chat = client.get(key)  # Retrieve data from Redis
    if chat:
        return json.loads(chat)  # Return the JSON-decoded data if found
    else:
        standard_key = 'suggestion-standard'  # Fallback to standard suggestions if specific suggestions are not found
        print("Searching for standard key:", standard_key)  # Log the fallback key being searched
        standard_chat = client.get(standard_key)  # Retrieve standard suggestions from Redis
        return json.loads(standard_chat) if standard_chat else []  # Return standard suggestions or an empty list

def check_suggestion_in_cache():
    # Check if there are any cached suggestions in Redis.
    
    # Returns:
    #     bool: True if suggestions are found in cache, otherwise False.
    pattern = "suggestion-"  # Pattern to match cached suggestion keys
    client = get_redis_client()  # Get Redis client instance
    for key in client.scan_iter(match=pattern):  # Iterate over keys matching the pattern
        return True  # Return True if any matching key is found
    return False  # Return False if no matching keys are found

def get_chat_from_cache(session_id):
    # Retrieve cached chat messages for a specific session ID from Redis.
    
    # Args:
    #     session_id (str): The unique identifier for the chat session.
    
    # Returns:
    #     list: The list of chat messages. If no messages are found, returns an empty list.
    client = get_redis_client()  # Get Redis client instance
    chat = client.get(session_id)  # Retrieve chat data from Redis
    return json.loads(chat) if chat else []  # Return the JSON-decoded data or an empty list if no data is found

def delete_chat_from_cache(session_id):
    # Delete cached chat messages for a specific session ID from Redis.
    
    # Args:
    #     session_id (str): The unique identifier for the chat session to be deleted.
    client = get_redis_client()  # Get Redis client instance
    client.delete(session_id)  # Remove the chat data from Redis

def update_message_in_cache(session_id, message_id, new_message):
    # Update a specific message within a chat session's cached data in Redis.
    
    # Args:
    #     session_id (str): The unique identifier for the chat session.
    #     message_id (str): The unique identifier for the message to be updated.
    #     new_message (str): The new content for the message.
    chat = get_chat_from_cache(session_id)  # Retrieve current chat data from cache
    for msg in chat:
        if msg['id'] == message_id:  # Find the message with the specified ID
            msg['message'] = new_message  # Update the message content
            break
    cache_chat(session_id, chat)  # Save the updated chat data back to Redis
