from kafka_consumer import KafkaConsumer
from logger import log_event
from validations import Intel
from pydantic import ValidationError
from mongo_client import mongo_instance
import math
import logger
from kafka_producer import kafka_producer


kafka_consumer = KafkaConsumer()

kafka_consumer.consume_data("intel")

mongo = mongo_instance

def process_intel(data):

    try:
        validate_data = Intel.model_validate(data)
        data_dict = validate_data.model_dump()
        query = {"entity_id": data_dict["entity_id"]}

        doc = mongo.collection.find(query)
        if doc:
            distance = haversine_km(doc["reported_lat"], doc["reported_lon"], data_dict["reported_lat"], data_dict["reported_lon"])
            mongo.collection.update_one({"entity_id": data_dict["entity_id"]}, {"$set":{"distance": distance}})

        else:
            mongo.collection.insert_one(data_dict)
            log_event("INFO", "add new target")

    except ValidationError as e:
        msg = {"data": data, "error": e}
        kafka_producer(msg, "intel_signals_dlq")




def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance in km between two points on Earth."""
    EARTH_RADIUS_KM = 6371.0

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c
