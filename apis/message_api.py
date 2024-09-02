from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.redis_service import get_redis_client, cache_chat, get_chat_from_cache, update_message_in_cache, delete_chat_from_cache
from utils.kafka_producer import produce_message
from uuid import uuid4
import json

router = APIRouter()
redis_client = get_redis_client()

class Message(BaseModel):
    session_id: str
    message: str

@router.post("/post")
def post_message(msg: Message):
   
    chat = get_chat_from_cache(msg.session_id)
    
    message_id = str(uuid4())
    
    chat.append({"id": message_id, "message": msg.message, "sender": "user"})
    
    chatbot_response = "This is a message from chatbot"
    chat.append({"id": str(uuid4()), "message": chatbot_response, "sender": "chatbot"})
    
    cache_chat(msg.session_id, chat)
    
    message_data = {
        "operation": "create",
        "session_id": msg.session_id,
        "message": msg.message,
        "chatbot_response": chatbot_response
    }
    
    # Debug logging
    print(f"Sending message data: {message_data}")
    
    produce_message(
        'chat-messages',
        msg.session_id.encode(),
        message_data  # Directly pass the dictionary
    )

    suggestions = [{"sid": "11aauuee", "suggestion_text": "suggestion 1 "},{"sid": "11aauu22", "suggestion_text": "suggestion 2"}, {"sid": "11aauu33", "suggestion_text": "suggestion 3"}]
    
    return {"user_message": msg.message, "chatbot_response": chatbot_response, "suggestions": suggestions}

@router.put("/edit")
def edit_message(session_id: str, message_id: str, new_message: str):
    update_message_in_cache(session_id, message_id, new_message)
    
    produce_message('chat-messages', key=session_id.encode(), value=json.dumps({"operation": "edit", "session_id": session_id, "message_id": message_id, "new_message": new_message}).encode())
    
    return {"message": "Message updated"}

@router.delete("/delete")
def delete_message(session_id: str, message_id: str):
    chat = get_chat_from_cache(session_id)
    
    chat = [msg for msg in chat if msg['id'] != message_id]
    chat = [msg for msg in chat if msg['sender'] != 'chatbot']
    
    cache_chat(session_id, chat)
    
    produce_message('chat-messages', key=session_id.encode(), value=json.dumps({"operation": "delete", "session_id": session_id, "message_id": message_id}).encode())
    
    return {"message": "Message deleted"}
