from validations import Attack
from mongo_client import mongo_instance
from logger import log_event
from pydantic import ValidationError
from kafka_producer import kafka_producer


mongo = mongo_instance

def process_attack(data):

    try:
        validate_data = Attack.model_validate(data)
        data_dict = validate_data.model_dump()
        query = {"entity_id": data_dict["entity_id"]}

        doc = mongo.collection.find(query)
        if doc:
            mongo.collection.update_one({"entity_id": data_dict["entity_id"]}, {"$set":{"is_attacked": True}})

        else:
            log_event("ERROR", "no such target")

    except ValidationError as e:
        msg = {"data": data, "error": e}
        kafka_producer(msg, "intel_signals_dlq")
