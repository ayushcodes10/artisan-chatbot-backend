from kafka import KafkaProducer, KafkaConsumer
import os
import json

producer = KafkaProducer(bootstrap_servers=os.getenv("KAFKA_BROKER"), value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_message_to_kafka(message):
    producer.send(os.getenv("KAFKA_TOPIC"), message)
    producer.flush()

def get_messages_from_kafka():
    consumer = KafkaConsumer(
        os.getenv("KAFKA_TOPIC"),
        bootstrap_servers=os.getenv("KAFKA_BROKER"),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='chatbot_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    for message in consumer:
        yield message.value
