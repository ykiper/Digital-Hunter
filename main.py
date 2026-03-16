from mongo_client import Mongodb
from kafka_consumer import KafkaConsumer



def main():
    kafka_consumer = KafkaConsumer()
    kafka_consumer.consume_data("Intel")
    kafka_consumer.consume_data("Attack")
    kafka_consumer.consume_data("Damage")

if __name__ == "__main__":
    main()