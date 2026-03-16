from confluent_kafka import Consumer
import json

consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "digital-hunter",
    "auto.offset.reset": "earliest"
}

class KafkaConsumer:

    def __init__(self):
        self.consumer = Consumer(consumer_config)

    def consume(self, topic_name):
        print("Consumer is running and subscribed to orders topic")

        self.consumer.subscribe([topic_name])

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print("Error:", msg.error())
                    continue

                value = msg.value().decode("utf-8")
                order = json.loads(value)
                print(f"Received order: {order['quantity']} x {order['item']} from {order['user']}")
        except KeyboardInterrupt:
            print("\nStopping consumer")
