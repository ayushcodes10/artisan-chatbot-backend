from fastapi import APIRouter, HTTPException
from services.database_service import SessionLocal
from database.models import ChatSession
import uuid
import json
from services.redis_service import cache_chat

router = APIRouter()

@router.post("/create")
def create_session():
    db = SessionLocal()
    session_id = str(uuid.uuid4())
    db_session = ChatSession(id=session_id)
    db.add(db_session)
    db.commit()
    
    # Initialize chat in Redis
    initial_message = {"id": str(uuid.uuid4()), "message": "Hi I am Ava, Helping you simplify state compliance for business accross the board. Can I get your name please?", "sender": "chatbot"}
    cache_chat(session_id, [initial_message])
    
    db.close()
    return {"session_id": session_id, "message": initial_message['message']}
