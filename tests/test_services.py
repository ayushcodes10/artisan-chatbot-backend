import pytest
from unittest.mock import patch, MagicMock
from services.message_service import get_message_response
from services.database_service import SessionLocal
from services.kafka_service import get_kafka_producer, get_kafka_consumer
from services.redis_service import (cache_chat, cache_suggestions, get_message_from_cache,
                                     check_suggestion_in_cache, get_chat_from_cache, delete_chat_from_cache,
                                     update_message_in_cache)
import json

@patch('services.kafka_service.KafkaProducer')
@patch('services.kafka_service.KafkaConsumer')
def test_get_kafka_producer(mock_kafka_producer, mock_kafka_consumer):
    # Test case for getting a Kafka producer.
    
    # It verifies that:
    # - The KafkaProducer is initialized with the correct configuration
    # - The producer's send method is called with the expected topic and message
    # - The producer returns the expected result

    # Mock the KafkaProducer and its send method
    mock_producer = MagicMock()
    mock_kafka_producer.return_value = mock_producer

    # Mock the future result of sending a message
    mock_future = MagicMock()
    mock_producer.send.return_value = mock_future
    mock_future.get.return_value = "success"

    # Call the function to get the Kafka producer
    producer = get_kafka_producer()
    
    # Assert that the producer is not None
    assert producer is not None
    
    # Verify that KafkaProducer was initialized with correct parameters
    mock_kafka_producer.assert_called_once_with(
        bootstrap_servers="kafka:9092",
        value_serializer=lambda v: json.dumps(v).encode('utf-8') if v is not None else None,
        key_serializer=lambda k: k if isinstance(k, bytes) else k.encode('utf-8') if k is not None else None
    )
    
    # Verify that the send method was called with the expected topic and message
    mock_producer.send.assert_called_once_with('test_topic', {'test': 'message'})

@patch('services.kafka_service.KafkaProducer')
@patch('services.kafka_service.KafkaConsumer')
def test_get_kafka_consumer(mock_kafka_producer, mock_kafka_consumer):
    # Test case for getting a Kafka consumer.
    
    # It verifies that:
    # - The KafkaConsumer is initialized with the correct configuration
    # - The consumer is set up to consume messages from the specified topic
    # - The partitions_for_topic method is called

    # Mock the KafkaConsumer and its methods
    mock_consumer = MagicMock()
    mock_kafka_consumer.return_value = mock_consumer

    # Mock the partitions_for_topic method
    mock_consumer.partitions_for_topic.return_value = {0}

    # Call the function to get the Kafka consumer
    consumer = get_kafka_consumer('test_topic')
    
    # Assert that the consumer is not None
    assert consumer is not None
    
    # Verify that KafkaConsumer was initialized with correct parameters
    mock_kafka_consumer.assert_called_once_with(
        'test_topic',
        bootstrap_servers="kafka:9092",
        value_deserializer=lambda m: json.loads(m.decode('utf-8')) if m else {},
        group_id='my-consumer-group',
        auto_offset_reset='earliest'
    )
    
    # Verify that the partitions_for_topic method was called
    assert mock_consumer.partitions_for_topic.called

@patch('services.redis_service.get_redis_client')
def test_cache_chat(mock_get_redis_client):
    # Test case for caching chat messages in Redis.
    
    # It verifies that:
    # - The chat messages are cached with the correct session ID
    # - The Redis set method is called with the expected data

    # Mock the Redis client
    mock_redis_client = MagicMock()
    mock_get_redis_client.return_value = mock_redis_client
    
    # Define test data
    session_id = 'test-session-id'
    messages = [{'id': '1', 'message': 'Hello', 'sender': 'user'}]
    
    # Call the function to cache chat messages
    cache_chat(session_id, messages)
    
    # Verify that the Redis set method was called with the correct parameters
    mock_redis_client.set.assert_called_once_with(session_id, json.dumps(messages))

@patch('services.redis_service.get_redis_client')
def test_cache_suggestions(mock_get_redis_client):
    # Test case for caching suggestions in Redis.
    
    # It verifies that:
    # - The suggestions are cached with the correct message
    # - The Redis set method is called with the expected data

    # Mock the Redis client
    mock_redis_client = MagicMock()
    mock_get_redis_client.return_value = mock_redis_client
    
    # Define test data
    message = 'test-message'
    data = {'response': 'How can I assist?', 'suggestions': ['Option 1', 'Option 2']}
    
    # Call the function to cache suggestions
    cache_suggestions(message, data)
    
    # Verify that the Redis set method was called with the correct parameters
    mock_redis_client.set.assert_called_once_with(f'suggestion-{message}', json.dumps(data))

@patch('services.redis_service.get_redis_client')
def test_get_message_from_cache(mock_get_redis_client):
    # Test case for retrieving a message from Redis cache.
    
    # It verifies that:
    # - The message is retrieved correctly from the cache
    # - The Redis get method is called with the expected parameters

    # Mock the Redis client
    mock_redis_client = MagicMock()
    mock_get_redis_client.return_value = mock_redis_client
    
    # Define test data
    message = 'test-message'
    mock_redis_client.get.side_effect = [json.dumps({'response': 'Response from cache', 'suggestions': ['Option 1']}), None]
    
    # Call the function to get the message from cache
    response = get_message_from_cache(message)
    
    # Verify the response data
    assert response['response'] == 'Response from cache'
    assert response['suggestions'] == ['Option 1']

@patch('services.redis_service.get_redis_client')
def test_check_suggestion_in_cache(mock_get_redis_client):
    # Test case for checking if suggestions exist in Redis cache.
    
    # It verifies that:
    # - The suggestions are checked correctly
    # - The Redis scan_iter method is called with the correct parameters

    # Mock the Redis client
    mock_redis_client = MagicMock()
    mock_get_redis_client.return_value = mock_redis_client
    
    # Mock the scan_iter method to return some suggestions
    mock_redis_client.scan_iter.return_value = ['suggestion-test-message']
    
    # Call the function to check if suggestions are in cache
    result = check_suggestion_in_cache()
    
    # Verify that the result is True
    assert result is True
    
    # Verify that scan_iter was called with the correct parameters
    mock_redis_client.scan_iter.assert_called_once_with(match='suggestion-')

@patch('services.redis_service.get_redis_client')
def test_get_chat_from_cache(mock_get_redis_client):
    # Test case for retrieving chat messages from Redis cache.
    
    # It verifies that:
    # - The chat messages are retrieved correctly from the cache
    # - The Redis get method is called with the expected parameters

    # Mock the Redis client
    mock_redis_client = MagicMock()
    mock_get_redis_client.return_value = mock_redis_client
    
    # Define test data
    session_id = 'test-session-id'
    chat_data = [{'id': '1', 'message': 'Hello', 'sender': 'user'}]
    mock_redis_client.get.return_value = json.dumps(chat_data)
    
    # Call the function to get the chat from cache
    chat = get_chat_from_cache(session_id)
    
    # Verify the retrieved chat data
    assert chat == chat_data
    
    # Verify that the Redis get method was called with the correct parameters
    mock_redis_client.get.assert_called_once_with(session_id)

@patch('services.redis_service.get_redis_client')
def test_delete_chat_from_cache(mock_get_redis_client):
    # Test case for deleting chat messages from Redis cache.
    
    # It verifies that:
    # - The chat messages are deleted correctly from the cache
    # - The Redis delete method is called with the expected parameters

    # Mock the Redis client
    mock_redis_client = MagicMock()
    mock_get_redis_client.return_value = mock_redis_client
    
    # Define test data
    session_id = 'test-session-id'
    
    # Call the function to delete the chat from cache
    delete_chat_from_cache(session_id)
    
    # Verify that the Redis delete method was called with the correct parameters
    mock_redis_client.delete.assert_called_once_with(session_id)

@patch('services.redis_service.get_redis_client')
def test_update_message_in_cache(mock_get_redis_client):
    # Test case for updating a message in Redis cache.
    
    # It verifies that:
    # - The message is updated correctly in the cache
    # - The Redis set method is called with the expected parameters

    # Mock the Redis client
    mock_redis_client = MagicMock()
    mock_get_redis_client.return_value = mock_redis_client
    
    # Define test data
    session_id = 'test-session-id'
    message_id = '1'
    new_message = 'Updated message'
    
    initial_chat = [{'id': message_id, 'message': 'Old message', 'sender': 'user'}]
    updated_chat = [{'id': message_id, 'message': new_message, 'sender': 'user'}]
    
    # Mock the Redis get method to return the initial chat data
    mock_redis_client.get.return_value = json.dumps(initial_chat)
    
    # Call the function to update the message in cache
    update_message_in_cache(session_id, message_id, new_message)
    
    # Verify that the Redis set method was called with the updated chat data
    mock_redis_client.set.assert_called_once_with(session_id, json.dumps(updated_chat))
