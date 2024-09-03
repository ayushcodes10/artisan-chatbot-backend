import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4

client = TestClient(app)

SESSION_ID = "test-session-id"
MESSAGE_ID = "test-message-id"
INVALID_SESSION_ID = "invalid-session-id"

def test_create_session():
    response = client.post("/sessions/create")
    assert response.status_code == 200
    response_json = response.json()
    assert "session_id" in response_json
    assert "message" in response_json
    assert isinstance(response_json["session_id"], str)
    assert isinstance(response_json["message"], str)

    initial_message = response_json["message"]
    assert initial_message == "Hi I am Ava, can I get your name?"

def test_post_message():
    response = client.post("/sessions/create")
    assert response.status_code == 200
    session_id = response.json()["session_id"]

    # Post a message
    response = client.post("/messages/post", json={
        "session_id": session_id,
        "message": "Hello, chatbot!"
    })
    assert response.status_code == 200
    response_json = response.json()
    assert "user_message" in response_json
    assert "chatbot_response" in response_json
    assert isinstance(response_json.get("suggestions"), list) 

def test_edit_message():
    response = client.post("/sessions/create")
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    client.post("/messages/post", json={
        "session_id": session_id,
        "message": "Hello, chatbot!"
    })
    
    response = client.put("/messages/edit", params={
        "session_id": session_id,
        "message_id": MESSAGE_ID,
        "new_message": "Updated message"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Message updated"}

def test_delete_message():
    response = client.post("/sessions/create")
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    client.post("/messages/post", json={
        "session_id": session_id,
        "message": "Hello, chatbot!"
    })
    
    response = client.delete("/messages/delete", params={
        "session_id": session_id,
        "message_id": MESSAGE_ID
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Message deleted"}
