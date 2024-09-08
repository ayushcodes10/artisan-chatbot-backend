from fastapi import FastAPI
from apis import session_api, message_api, health_check
import threading
from utils.kafka_consumer import consume_messages  
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

consumer_thread = threading.Thread(target=consume_messages, daemon=True)
consumer_thread.start()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session_api.router, prefix="/sessions")
app.include_router(message_api.router, prefix="/messages")
app.include_router(health_check.router, prefix="/health")


