# Import necessary SQLAlchemy classes and functions for defining models and their properties
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, ARRAY
from sqlalchemy.dialects.postgresql import UUID  # Import UUID data type for PostgreSQL
from sqlalchemy.orm import relationship  # Import relationship function to define relationships between models
from sqlalchemy.sql import func  # Import func to use SQL functions like now() for default timestamps
import uuid  # Import uuid to generate unique identifiers
from services.database_service import Base  # Import Base from the database service to define models

# Define the ChatSession model which represents a chat session in the database
class ChatSession(Base):
    __tablename__ = 'chat_sessions'  # Name of the table in the database

    # Unique identifier for each chat session, using UUID as the primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Unique session ID for the chat session, indexed for faster queries
    session_id = Column(String, unique=True, index=True)
    
    # Relationship to ChatMessage, indicating that each session can have multiple messages
    messages = relationship("ChatMessage", back_populates="session")

# Define the ChatMessage model which represents individual chat messages within a session
class ChatMessage(Base):
    __tablename__ = 'chat_messages'  # Name of the table in the database

    # Unique identifier for each chat message, using UUID as the primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key linking the message to a specific chat session
    session_id = Column(UUID(as_uuid=True), ForeignKey('chat_sessions.id'))
    
    # The content of the chat message
    message = Column(Text)
    
    # Timestamp of when the message was created, defaults to the current time
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to ChatSession, indicating the session this message belongs to
    session = relationship("ChatSession", back_populates="messages")
    
    # The sender of the message, typically either 'user' or 'chatbot'
    sender = Column(String)

# Define the ChatbotMessageSuggestion model which represents possible suggestions generated by the chatbot
class ChatbotMessageSuggestion(Base):
    __tablename__ = 'chatbot_messages_suggestions'  # Name of the table in the database
    
    # Unique identifier for each suggestion record
    id = Column(Integer, primary_key=True)
    
    # The message that the suggestions are related to
    message = Column(String)
    
    # An array of text suggestions provided by the chatbot
    suggestions = Column(ARRAY(Text))
    
    # The actual response given by the chatbot
    response = Column(Text)
