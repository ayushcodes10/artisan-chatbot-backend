from services.kafka_service import get_kafka_consumer
from services.database_service import SessionLocal
from database.models import ChatMessage, ChatSession
from uuid import uuid4


import json



def consume_messages():
    try: 
        consumer = get_kafka_consumer('chat-messages')
        for message in consumer:
            try:
                print(f"Received message: {message.value.decode()}")
                process_message(message.value.decode())
            except Exception as e:
                print(f"Error processing message: {e}")
        

    except Exception as e:
        print(f"Error while starting Kafka consumer: {e}")

def process_message(message_str):
    data = json.loads(message_str)
    operation = data['operation']
    session_id = data['session_id']
    
    db = SessionLocal()
    try:
        print("Processing queue", data)
        if operation == 'create':
            user_message = data['message']
            chatbot_response = data['chatbot_response']
            db.add(ChatMessage(id=str(uuid4()), session_id=session_id, message=user_message, sender='user'))
            db.add(ChatMessage(id=str(uuid4()), session_id=session_id, message=chatbot_response, sender='chatbot'))
        
        elif operation == 'edit':
            message_id = data['message_id']
            new_message = data['new_message']
            msg = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
            if msg:
                msg.message = new_message
                db.query(ChatMessage).filter(ChatMessage.session_id == session_id, ChatMessage.sender == 'chatbot').delete()
                db.add(ChatMessage(id=str(uuid4()), session_id=session_id, message="This is a message from chatbot", sender='chatbot'))
        
        elif operation == 'delete':
            message_id = data['message_id']
            db.query(ChatMessage).filter(ChatMessage.id == message_id).delete()
            db.query(ChatMessage).filter(ChatMessage.session_id == session_id, ChatMessage.sender == 'chatbot').delete()
        
        db.commit()
    except Exception as e:
        print(f"Error processing message: {e}")
        db.rollback()
    finally:
        db.close()
