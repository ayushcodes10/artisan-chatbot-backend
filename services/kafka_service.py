from kafka import KafkaProducer, KafkaConsumer, errors
import time
import os
import json

def get_kafka_producer():
    kafka_broker = os.getenv("KAFKA_BROKER", "kafka:9092")
    max_retries = 3
    retry_interval = 15  # seconds
    
    for attempt in range(max_retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=kafka_broker,
                value_serializer=lambda v: json.dumps(v).encode('utf-8') if v is not None else None,  
                key_serializer=lambda k: k if isinstance(k, bytes) else k.encode('utf-8') if k is not None else None  
            )
           
            future = producer.send('test_topic', {'test': 'message'})
            result = future.get(timeout=10)
            print("Producer initialization successful:", result)
            return producer
        except errors.NoBrokersAvailable as e:
            print(f"Attempt {attempt + 1} of {max_retries}: No Kafka brokers available. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
        except Exception as e:
            
            print(f"Attempt {attempt + 1} of {max_retries}: Error while creating Kafka producer: {e}")
            time.sleep(retry_interval)
    
    raise Exception("Failed to connect to Kafka brokers after multiple attempts.")

def get_kafka_consumer(topic):
    kafka_broker = os.getenv("KAFKA_BROKER", "kafka:9092")
    max_retries = 3
    retry_interval = 15  
    
    for attempt in range(max_retries):
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=kafka_broker,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')) if m else {}, 
                group_id='my-consumer-group',
                auto_offset_reset='earliest'
            )
            
           
            partitions = list(consumer.partitions_for_topic(topic) or [])
            if partitions:
                print("Consumer initialization successful. Partitions:", partitions)
            else:
                print("No partitions found for topic:", topic)
            return consumer
        
        except errors.NoBrokersAvailable as e:
            print(f"Attempt {attempt + 1} of {max_retries}: No Kafka brokers available for consumer. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
        
        except Exception as e:
            
            print(f"Attempt {attempt + 1} of {max_retries}: Error while creating Kafka consumer: {e}")
            time.sleep(retry_interval)
    
    raise Exception("Failed to connect to Kafka brokers after multiple attempts.")
