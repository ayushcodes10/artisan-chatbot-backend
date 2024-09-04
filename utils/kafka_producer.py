# Import the function to get a Kafka producer
from services.kafka_service import get_kafka_producer

def produce_message(topic, key, value):
    
    # Produce a message to a Kafka topic.

    # Args:
    #     topic (str): The Kafka topic to which the message will be sent.
    #     key (str or bytes): The key of the Kafka message. Must be a string or bytes.
    #     value (any): The value of the Kafka message. Can be any serializable object.

    # Raises:
    #     ValueError: If the key is neither a string nor bytes.

    try:
        # Obtain a Kafka producer instance
        producer = get_kafka_producer()
        
        # Ensure the key is in bytes format
        if isinstance(key, str):
            key = key.encode('utf-8')
        elif not isinstance(key, bytes):
            # Raise an error if the key is not a string or bytes
            raise ValueError("Key must be a string or bytes.")
        
        # Send the message to the specified Kafka topic
        result = producer.send(topic, key=key, value=value)
        # Wait for the message to be acknowledged and get the result
        r1 = result.get(timeout=10)
        print("Producer result", r1)  # Print the result for debugging purposes
        
        # Ensure all messages are sent before returning
        producer.flush()
        
    except Exception as e:
        # Log any errors encountered during message sending
        print(f"Error while sending message to Kafka: {e}")
