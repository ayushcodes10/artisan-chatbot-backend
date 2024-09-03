# Chat Application

This project is a chat application built using FastAPI, PostgreSQL, Redis, and Kafka. It features a backend that handles real-time chat interactions, message management, and session management. The application is containerized using Docker for ease of deployment and scalability.

## Project Structure

- `main.py`: Main entry point for the FastAPI application. Includes API routes for sessions, messages, and health checks.
- `message_api.py`: API routes for handling chat messages (create, edit, delete).
- `session_api.py`: API routes for managing chat sessions.
- `services/`: Contains service modules for interacting with Redis, PostgreSQL, and Kafka.
- `utils/`: Contains utility modules for Kafka producers and consumers.
- `Dockerfile`: Docker configuration file for building the application container.
- `docker-compose.yml`: Docker Compose configuration for setting up multi-container Docker applications.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### 1. Clone the Repository

```
git clone <repository-url>
cd <repository-directory>
```

### 2. Configure Environment Variables
Create a .env file in the root directory and add the following environment variables:

```bash
POSTGRES_URL=postgres://user:password@postgres:5432/chatdb
REDIS_URL=redis://redis:6379/0
KAFKA_BROKER=kafka:9093
```

### 3. Build and Run the Application
```
docker-compose up --build
```

This command will build and start all the required containers, including FastAPI, PostgreSQL, Redis, and Kafka.

### 4. Access the Application
The application will be available at http://localhost:8000. You can use tools like Postman or cURL to interact with the API endpoints.

## API Endpoints
### Sessions
- POST /sessions/create: Creates a new chat session and initializes it with a welcome message.
### Messages
- POST /messages/post: Posts a new message to the chat and receives a response from the chatbot.
- PUT /messages/edit: Edits an existing message.
- DELETE /messages/delete: Deletes a message from the chat.
### Health Check
- GET /health: Checks the health status of the application.

## Usage of Kafka and Redis
### Kafka
Apache Kafka is used in this project for handling real-time event streaming and message production/consumption. Here’s how Kafka is integrated:

- Message Production: The produce_message function sends messages related to chat operations (e.g., creating, editing, deleting messages) to a Kafka topic (chat-messages). This allows asynchronous processing and decouples the chat operations from other system components.
- Message Consumption: While the current implementation does not include a Kafka consumer, it is typically used to process or handle incoming messages from Kafka topics. Consumers can be added to process chat messages in real-time.

### Redis
Redis is used in this project for fast access to cached data and session management. Here’s how Redis is integrated:

- Caching Chat Messages: The cache_chat function stores chat messages in Redis. This allows quick retrieval of chat history without repeatedly querying the PostgreSQL database, improving performance and reducing database load.
- Caching Suggestions: The cache_suggestions function stores message suggestions in Redis. The get_message_from_cache function retrieves suggestions from Redis, improving response times by avoiding repeated database queries.
- Session Management: Redis is used to manage chat sessions, storing session data and messages in memory for quick access.
By utilizing Kafka and Redis, this chat application achieves improved scalability, responsiveness, and performance. Kafka manages real-time messaging and event processing, while Redis ensures fast access to frequently used data and efficient session management.

## Running Tests
To run the automated test cases for the API endpoints and services, use the following command:
```
pytest
```
Ensure that Docker containers are running when executing tests, as they rely on the availability of the services defined in docker-compose.yml.