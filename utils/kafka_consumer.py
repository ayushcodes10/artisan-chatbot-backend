from services.kafka_service import get_kafka_consumer
from services.database_service import SessionLocal
from database.models import ChatMessage, ChatSession
from uuid import uuid4, UUID


import json

def consume_messages():
    try: 
        consumer = get_kafka_consumer('chat-messages')
        for message in consumer:
            try:
                message_value_str = json.dumps(message.value)
                print(f"Received message: {message_value_str}")
                process_message(message_value_str)
            except Exception as e:
                print(f"Error processing message in consumer: {e}")
        

    except Exception as e:
        print(f"Error while starting Kafka consumer: {e}")

def process_message(message_str):
    data = json.loads(message_str)
    operation = data['operation']
    session_id = UUID(data['session_id']) 
    message_id = UUID(data.get('message_id')) if 'message_id' in data else None
    
    db = SessionLocal()
    try:
        print("Processing queue", data)
        if operation == 'create':
            user_message = data['message']
            chatbot_response = data['chatbot_response']
            db.add(ChatMessage(id=uuid4(), session_id=session_id, message=user_message, sender='user'))
            db.add(ChatMessage(id=uuid4(), session_id=session_id, message=chatbot_response, sender='chatbot'))
        
        elif operation == 'edit':
            new_message = data['new_message']
            if message_id:
                msg = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
                if msg:
                    msg.message = new_message
                    db.query(ChatMessage).filter(ChatMessage.session_id == session_id, ChatMessage.sender == 'chatbot').delete()
                    db.add(ChatMessage(id=uuid4(), session_id=session_id, message="This is a message from chatbot", sender='chatbot'))
        
        elif operation == 'delete':
            if message_id:
                db.query(ChatMessage).filter(ChatMessage.id == message_id).delete()
            db.query(ChatMessage).filter(ChatMessage.session_id == session_id, ChatMessage.sender == 'chatbot').delete()
        
        db.commit()
    except Exception as e:
        print(f"Error processing message: {e}")
        db.rollback()
    finally:
        db.close()