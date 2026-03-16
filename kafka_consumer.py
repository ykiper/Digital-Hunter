from confluent_kafka import Consumer
import json
from logger import log_event
from intel_processor import process_intel
from attack_processor import process_attack

consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "digital-hunter",
    "auto.offset.reset": "earliest"
}

class KafkaConsumer:

    def __init__(self):
        self.consumer = Consumer(consumer_config)

    def consume_data(self, topic_name):

        self.consumer.subscribe([topic_name])
        log_event("INFO", f"Consumer is running and subscribed to {topic_name} topic")

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    log_event("ERROR", msg.error())
                    continue

                value = msg.value().decode("utf-8")
                event = json.loads(value)
                if topic_name == "Intel":
                    process_intel(event)
                elif topic_name == "Attack":
                    process_attack(event)

        except KeyboardInterrupt:
            print("\nStopping consumer")
