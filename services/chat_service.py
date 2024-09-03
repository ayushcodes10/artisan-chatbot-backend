from services.redis_service import get_chat_from_cache
from services.database_service import SessionLocal
from database.models import ChatbotMessageSuggestion
from services.redis_service import cache_suggestions, get_message_from_cache, check_suggestion_in_cache
import json

def get_message_response(session_id, message):
     db = SessionLocal()

     if  not check_suggestion_in_cache() : 
          suggestions = db.query(ChatbotMessageSuggestion).all()
          print("suggestions", suggestions)
          for suggestion in suggestions:

               data = {
                    "suggestions": suggestion.suggestions,
                    "response": suggestion.response
               }

               cache_suggestions(suggestion.message, json.dumps(data))

     chat = get_chat_from_cache(session_id)
     response = {}
     if(len(chat) < 3) :
         response = get_message_from_cache("usersname")
     else:
          response = get_message_from_cache(message)
     
     print ("message response from cache", response)
     return json.loads(response)