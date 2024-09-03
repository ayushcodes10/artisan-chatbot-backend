from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from services.database_service import Base  

class ChatSession(Base):
    __tablename__ = 'chat_sessions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    session_id = Column(String, unique=True, index=True)
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    session_id = Column(UUID(as_uuid=True), ForeignKey('chat_sessions.id'))
    message = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    session = relationship("ChatSession", back_populates="messages")
    sender = Column(String) 

class ChatbotMessageSuggestion(Base):
    __tablename__ = 'chatbot_messages_suggestions'
    
    id = Column(Integer, primary_key=True)
    message = Column(String)
    suggestions = Column(ARRAY(Text))
    response = Column(Text)
