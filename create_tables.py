from services.database_service import engine, Base
from database.models import ChatSession, ChatMessage

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()