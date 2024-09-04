# Import necessary modules and functions
from services.kafka_service import get_kafka_consumer  # Function to initialize Kafka consumer
from services.database_service import SessionLocal  # Function to create a database session
from database.models import ChatMessage, ChatSession  # Database models for chat messages and sessions
from uuid import uuid4, UUID  # UUID utilities for generating and parsing UUIDs
import json  # Library for handling JSON data

def consume_messages():
    # Consume messages from Kafka topic 'chat-messages', process each message,
    # and handle any exceptions that occur during consumption and processing.
    try:
        # Initialize Kafka consumer for the 'chat-messages' topic
        consumer = get_kafka_consumer('chat-messages')
        
        # Continuously poll for new messages from Kafka
        for message in consumer:
            try:
                # Convert Kafka message value to JSON string for processing
                message_value_str = json.dumps(message.value)
                print(f"Received message: {message_value_str}")
                
                # Process the received message
                process_message(message_value_str)
                
            except Exception as e:
                # Log errors that occur while processing the message
                print(f"Error processing message in consumer: {e}")

    except Exception as e:
        # Log errors that occur while starting the Kafka consumer
        print(f"Error while starting Kafka consumer: {e}")

def process_message(message_str):
    # Process a message by performing operations (create, edit, delete) on chat messages
    # based on the operation specified in the message.
    
    # Args:
    #     message_str (str): JSON string containing the message data.

    # Parse the JSON message string
    data = json.loads(message_str)
    operation = data['operation']  # Extract the operation type (create, edit, delete)
    session_id = UUID(data['session_id'])  # Extract and convert session_id to UUID
    message_id = UUID(data.get('message_id')) if 'message_id' in data else None  # Extract message_id if present

    # Create a new database session
    db = SessionLocal()
    try:
        print("Processing queue", data)  # Log the data being processed

        # Handle 'create' operation: add new messages to the database
        if operation == 'create':
            user_message = data['message']
            chatbot_response = data['chatbot_response']
            # Add user message to the database
            db.add(ChatMessage(id=uuid4(), session_id=session_id, message=user_message, sender='user'))
            # Add chatbot response to the database
            db.add(ChatMessage(id=uuid4(), session_id=session_id, message=chatbot_response, sender='chatbot'))

        # Handle 'edit' operation: update an existing message in the database
        elif operation == 'edit':
            new_message = data['new_message']
            if message_id:
                # Find the message to be updated
                msg = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
                if msg:
                    # Update the message content
                    msg.message = new_message
                    # Delete existing chatbot messages for the session
                    db.query(ChatMessage).filter(ChatMessage.session_id == session_id, ChatMessage.sender == 'chatbot').delete()
                    # Add a new chatbot message
                    db.add(ChatMessage(id=uuid4(), session_id=session_id, message="This is a message from chatbot", sender='chatbot'))

        # Handle 'delete' operation: remove a message from the database
        elif operation == 'delete':
            if message_id:
                # Delete the specific message
                db.query(ChatMessage).filter(ChatMessage.id == message_id).delete()
            # Delete all chatbot messages for the session
            db.query(ChatMessage).filter(ChatMessage.session_id == session_id, ChatMessage.sender == 'chatbot').delete()

        # Commit the transaction to save changes
        db.commit()
        
    except Exception as e:
        # Log errors that occur during message processing and rollback the transaction
        print(f"Error processing message: {e}")
        db.rollback()
        
    finally:
        # Close the database session
        db.close()
