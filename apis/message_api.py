# Import necessary modules and classes from FastAPI and other services
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.redis_service import (
    get_redis_client, 
    cache_chat, 
    get_chat_from_cache, 
    update_message_in_cache, 
    delete_chat_from_cache
)
from utils.kafka_producer import produce_message
from services.chat_service import get_message_response
from uuid import uuid4
import json

# Initialize a FastAPI router for organizing the endpoints
router = APIRouter()

# Initialize the Redis client to interact with the Redis cache
redis_client = get_redis_client()

# Define a Pydantic model for validating the incoming request data
class Message(BaseModel):
    session_id: str  # Session identifier for the chat
    message: str     # User's message to the chatbot

# Endpoint to handle posting a new message in a chat session
@router.post("/post")
def post_message(msg: Message):
    # Retrieve the current chat session from the cache using the session_id
    chat = get_chat_from_cache(msg.session_id)
    
    # Generate a unique ID for the new user message
    message_id = str(uuid4())
    
    # Append the new user message to the chat history
    chat.append({"id": message_id, "message": msg.message, "sender": "user"})
    
    # Get the chatbot's response based on the user's message
    response = get_message_response(msg.session_id, msg.message)
    chatbot_response = response["response"]
    
    # Append the chatbot's response to the chat history
    chat.append({"id": str(uuid4()), "message": chatbot_response, "sender": "chatbot"})
    
    # Cache the updated chat session in Redis
    cache_chat(msg.session_id, chat)
    
    # Prepare data for producing a Kafka message
    message_data = {
        "operation": "create",               # Operation type
        "session_id": msg.session_id,        # Session ID
        "message": msg.message,              # User message
        "chatbot_response": chatbot_response # Chatbot's response
    }
    
    # Produce a message to the Kafka topic 'chat-messages'
    produce_message(
        'chat-messages',           # Kafka topic
        msg.session_id.encode(),   # Partition key as session_id
        message_data               # Message value as the serialized data
    )

    # Extract suggested responses from the chatbot's response
    suggestions = response["suggestions"]
    
    # Return the user message, chatbot response, and suggestions in the API response
    return {"user_message": msg.message, "chatbot_response": chatbot_response, "suggestions": suggestions}

# Endpoint to handle deleting the last user and chatbot messages from a chat session
@router.delete("/delete")
def delete_last_messages(session_id: str):
    # Retrieve the current chat session from the cache using the session_id
    chat = get_chat_from_cache(session_id)
    
    # Find the last user message
    last_user_index = None
    last_chatbot_index = None
    
    # Iterate over the messages to find the last user message and the corresponding chatbot message
    for i in range(len(chat) - 1, -1, -1):
        if chat[i]['sender'] == 'user' and last_user_index is None:
            last_user_index = i
        elif chat[i]['sender'] == 'chatbot' and last_user_index is not None:
            last_chatbot_index = i
            break  # Stop once the chatbot response corresponding to the last user message is found
    
    # If both messages are found, delete them
    if last_user_index is not None and last_chatbot_index is not None:
        # Remove the last user message and the corresponding chatbot message from the chat
        del chat[last_user_index]
        del chat[last_chatbot_index - 1]  # Adjust the index after removing the user message
    
    # Cache the updated chat session in Redis
    cache_chat(session_id, chat)
    
    # Produce a Kafka message indicating the delete operation
    produce_message(
        'chat-messages', 
        key=session_id.encode(), 
        value=json.dumps({
            "operation": "delete",         # Operation type
            "session_id": session_id,      # Session ID
            "message_type": "last"         # Indicates the last messages were deleted
        }).encode()
    )
    
    # Return a success message
    return {"message": "Last user and chatbot messages deleted"}

# Endpoint to handle editing an existing message in a chat session
@router.put("/edit")
def edit_message(session_id: str, new_message: str):
    # Step 1: Delete the last user and chatbot messages
    delete_last_messages(session_id)

    # Step 2: Create a new message with the updated content
    message_data = Message(session_id=session_id, message=new_message)
    return post_message(message_data)
