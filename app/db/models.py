from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.session_id"))
    message_text = Column(String)
    message_type = Column(String)  # 'user' or 'bot'
    timestamp = Column(DateTime, default=datetime.utcnow)
    session = relationship("Session", back_populates="messages")

Session.messages = relationship("Message", back_populates="session")
