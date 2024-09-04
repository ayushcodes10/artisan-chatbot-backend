# Import necessary modules and classes from FastAPI and other services
from fastapi import APIRouter, HTTPException
from services.database_service import SessionLocal  # Importing the database session manager
from database.models import ChatSession  # Importing the ChatSession model from the database models
import uuid  # Importing the uuid module to generate unique session IDs
import json  # Importing json for handling JSON data (though not used directly in this code)
from services.redis_service import cache_chat  # Importing the caching function to store chat data in Redis

# Initialize a FastAPI router for organizing the endpoints
router = APIRouter()

# Endpoint to handle the creation of a new chat session
@router.post("/create")
def create_session():
    # Create a new database session for interacting with the database
    db = SessionLocal()
    
    # Generate a unique session ID for the new chat session
    session_id = str(uuid.uuid4())
    
    # Create a new ChatSession object with the generated session ID
    db_session = ChatSession(id=session_id)
    
    # Add the new session to the database
    db.add(db_session)
    
    # Commit the transaction to save the new session in the database
    db.commit()
    
    # Initialize the chat in Redis with the first message from the chatbot
    initial_message = {
        "id": str(uuid.uuid4()),  # Generate a unique ID for the initial message
        "message": "Hi I am Ava, Helping you simplify state compliance for business across the board. Can I get your name please?",  # Initial message from the chatbot
        "sender": "chatbot"  # Sender identifier (chatbot)
    }
    
    # Cache the initial chat message in Redis using the session ID as the key
    cache_chat(session_id, [initial_message])
    
    # Close the database session to release the connection
    db.close()
    
    # Return the session ID and the initial chatbot message in the API response
    return {"session_id": session_id, "message": initial_message['message']}
