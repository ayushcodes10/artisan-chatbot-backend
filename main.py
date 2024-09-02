from fastapi import FastAPI
from apis import session_api, message_api, health_check
import threading
from utils.kafka_consumer import consume_messages

app = FastAPI()

app.include_router(session_api.router, prefix="/sessions")
app.include_router(message_api.router, prefix="/messages")
app.include_router(health_check.router, prefix="/health")

# Start the consumer in a separate thread
def start_consumer():
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.daemon = True
    consumer_thread.start()

# Initialize the application
if __name__ == "__main__":
    start_consumer()  # Start the Kafka consumer in a background thread
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

