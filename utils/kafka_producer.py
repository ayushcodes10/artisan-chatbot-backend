from services.kafka_service import get_kafka_producer
def produce_message(topic, key, value):
    try:
        producer = get_kafka_producer()
        
        if isinstance(key, str):
            key = key.encode('utf-8')
        elif not isinstance(key, bytes):
            raise ValueError("Key must be a string or bytes.")
        
        producer.send(topic, key=key, value=value)
        producer.flush()
        
    except Exception as e:
        print(f"Error while sending message to Kafka: {e}")
