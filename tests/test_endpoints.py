import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4

# Initialize the TestClient with the FastAPI application
client = TestClient(app)

# Define constants for session and message IDs used in tests
SESSION_ID = "test-session-id"
MESSAGE_ID = "test-message-id"
INVALID_SESSION_ID = "invalid-session-id"

def test_create_session():
    # Test case for creating a new session.
    
    # It checks that the response:
    # - Returns a status code of 200
    # - Contains a session_id and a message in the response JSON
    # - Ensures that the session_id and message are of type string
    # - Confirms that the initial message is as expected

    response = client.post("/sessions/create")
    
    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    # Parse the response JSON
    response_json = response.json()
    
    # Assert that session_id and message are present in the response
    assert "session_id" in response_json
    assert "message" in response_json
    
    # Assert that session_id and message are strings
    assert isinstance(response_json["session_id"], str)
    assert isinstance(response_json["message"], str)
    
    # Assert that the initial message is as expected
    initial_message = response_json["message"]
    assert initial_message == "Hi I am Ava, can I get your name?"

def test_post_message():
    # Test case for posting a message to a session.
    
    # It checks that:
    # - A session is created successfully
    # - A message is posted successfully
    # - The response contains the user_message, chatbot_response, and suggestions
    # - Suggestions, if present, are in a list format

    # Create a new session
    response = client.post("/sessions/create")
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    
    # Post a message to the created session
    response = client.post("/messages/post", json={
        "session_id": session_id,
        "message": "Hello, chatbot!"
    })
    
    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    # Parse the response JSON
    response_json = response.json()
    
    # Assert that the response contains user_message and chatbot_response
    assert "user_message" in response_json
    assert "chatbot_response" in response_json
    
    # Assert that suggestions are in a list format, if present
    assert isinstance(response_json.get("suggestions"), list) 

def test_edit_message():
    # Test case for editing a message in a session.
    
    # It checks that:
    # - A session is created successfully
    # - A message is posted to the session
    # - The message is edited successfully
    # - The response confirms that the message was updated

    # Create a new session
    response = client.post("/sessions/create")
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    
    # Post a message to the created session
    client.post("/messages/post", json={
        "session_id": session_id,
        "message": "Hello, chatbot!"
    })
    
    # Edit the posted message
    response = client.put("/messages/edit", params={
        "session_id": session_id,
        "message_id": MESSAGE_ID,
        "new_message": "Updated message"
    })
    
    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    # Assert that the response confirms the message was updated
    assert response.json() == {"message": "Message updated"}

def test_delete_message():
    # Test case for deleting a message from a session.
    
    # It checks that:
    # - A session is created successfully
    # - A message is posted to the session
    # - The message is deleted successfully
    # - The response confirms that the message was deleted

    # Create a new session
    response = client.post("/sessions/create")
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    
    # Post a message to the created session
    client.post("/messages/post", json={
        "session_id": session_id,
        "message": "Hello, chatbot!"
    })
    
    # Delete the posted message
    response = client.delete("/messages/delete", params={
        "session_id": session_id,
        "message_id": MESSAGE_ID
    })
    
    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    # Assert that the response confirms the message was deleted
    assert response.json() == {"message": "Message deleted"}
