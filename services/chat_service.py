# Import necessary functions and classes from other services and libraries
from services.redis_service import get_chat_from_cache  # Function to get chat data from Redis cache
from services.database_service import SessionLocal  # Database session management
from database.models import ChatbotMessageSuggestion  # Database model for chatbot message suggestions
from services.redis_service import cache_suggestions, get_message_from_cache, check_suggestion_in_cache  # Redis functions for caching and retrieving suggestions
import json  # Module for handling JSON data

# Function to get a chatbot response based on the user's message and session ID
def get_message_response(session_id, message):
    db = SessionLocal()  # Create a new database session

    # Check if suggestions are already cached; if not, cache them from the database
    if not check_suggestion_in_cache():
        # Query all suggestions from the database
        suggestions = db.query(ChatbotMessageSuggestion).all()
        print("suggestions", suggestions)  # Debugging print statement to show the retrieved suggestions
        
        # Cache each suggestion in Redis
        for suggestion in suggestions:
            data = {
                "suggestions": suggestion.suggestions,  # Store the suggestions
                "response": suggestion.response  # Store the chatbot's response
            }

            # Cache the suggestion in Redis with the message as the key
            cache_suggestions(suggestion.message, json.dumps(data))

    # Retrieve the chat history for the given session ID from the Redis cache
    chat = get_chat_from_cache(session_id)
    
    # Initialize an empty dictionary to hold the response data
    response = {}
    
    # Determine the response based on the number of messages in the chat history
    if len(chat) < 3:
        # If the chat has fewer than 3 messages, get a general response (like asking for the user's name)
        response = get_message_from_cache("usersname")
    else:
        # If the chat has more than 3 messages, get a response based on the current message
        response = get_message_from_cache(message)
    
    print("message response from cache", response)  # Debugging print statement to show the response retrieved from cache
    
    # Return the response after converting it from JSON format to a Python dictionary
    return json.loads(response)
