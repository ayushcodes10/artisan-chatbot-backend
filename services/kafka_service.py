# Import necessary modules from Kafka, time for delays, os for environment variables, and json for serialization
from kafka import KafkaProducer, KafkaConsumer, errors
import time
import os
import json

def get_kafka_producer():
    # Retrieve Kafka broker address from environment variable, defaulting to "kafka:9092"
    kafka_broker = os.getenv("KAFKA_BROKER", "kafka:9092")
    
    # Define the maximum number of retry attempts and the interval between retries (in seconds)
    max_retries = 3
    retry_interval = 15  # seconds
    
    # Attempt to create a KafkaProducer instance with retry logic
    for attempt in range(max_retries):
        try:
            # Initialize KafkaProducer with specified settings
            producer = KafkaProducer(
                bootstrap_servers=kafka_broker,  # Kafka broker address
                value_serializer=lambda v: json.dumps(v).encode('utf-8') if v is not None else None,  # Serialize message values as JSON
                key_serializer=lambda k: k if isinstance(k, bytes) else k.encode('utf-8') if k is not None else None  # Serialize message keys as bytes
            )
           
            # Send a test message to ensure producer is working
            future = producer.send('test_topic', {'test': 'message'})
            result = future.get(timeout=10)  # Wait for message to be acknowledged
            print("Producer initialization successful:", result)  # Log success
            return producer  # Return the producer instance
        
        except errors.NoBrokersAvailable as e:
            # Handle case where no Kafka brokers are available
            print(f"Attempt {attempt + 1} of {max_retries}: No Kafka brokers available. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)  # Wait before retrying
        
        except Exception as e:
            # Handle any other exceptions
            print(f"Attempt {attempt + 1} of {max_retries}: Error while creating Kafka producer: {e}")
            time.sleep(retry_interval)  # Wait before retrying
    
    # Raise an exception if connection to Kafka brokers fails after multiple attempts
    raise Exception("Failed to connect to Kafka brokers after multiple attempts.")

def get_kafka_consumer(topic):
    # Retrieve Kafka broker address from environment variable, defaulting to "kafka:9092"
    kafka_broker = os.getenv("KAFKA_BROKER", "kafka:9092")
    
    # Define the maximum number of retry attempts and the interval between retries (in seconds)
    max_retries = 3
    retry_interval = 15  # seconds
    
    # Attempt to create a KafkaConsumer instance with retry logic
    for attempt in range(max_retries):
        try:
            # Initialize KafkaConsumer with specified settings
            consumer = KafkaConsumer(
                topic,  # Topic to consume messages from
                bootstrap_servers=kafka_broker,  # Kafka broker address
                value_deserializer=lambda m: json.loads(m.decode('utf-8')) if m else {},  # Deserialize message values from JSON
                group_id='my-consumer-group',  # Consumer group ID
                auto_offset_reset='earliest'  # Start reading from the earliest message if no offset is committed
            )
            
            # Check the partitions assigned to the consumer for the specified topic
            partitions = list(consumer.partitions_for_topic(topic) or [])
            if partitions:
                print("Consumer initialization successful. Partitions:", partitions)  # Log success and partitions
            else:
                print("No partitions found for topic:", topic)  # Log if no partitions found
            return consumer  # Return the consumer instance
        
        except errors.NoBrokersAvailable as e:
            # Handle case where no Kafka brokers are available
            print(f"Attempt {attempt + 1} of {max_retries}: No Kafka brokers available for consumer. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)  # Wait before retrying
        
        except Exception as e:
            # Handle any other exceptions
            print(f"Attempt {attempt + 1} of {max_retries}: Error while creating Kafka consumer: {e}")
            time.sleep(retry_interval)  # Wait before retrying
    
    # Raise an exception if connection to Kafka brokers fails after multiple attempts
    raise Exception("Failed to connect to Kafka brokers after multiple attempts.")
