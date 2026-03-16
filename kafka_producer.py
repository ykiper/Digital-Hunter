import json
from confluent_kafka import Producer

def kafka_producer(value, topic):

    producer_config = {
        "bootstrap.servers": "localhost:9092"
    }

    producer = Producer(producer_config)
    encode_value = json.dumps(value).encode("utf-8")
    producer.produce(
        topic=topic,
        value=encode_value
    )
    producer.flush()