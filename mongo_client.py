from pymongo import MongoClient

from intel_processor import mongo
from logger import log_event

class Mongodb:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["hunter"]
        self.collection = self.db["intel_bank"]

    def save(self, data):
        try:
            self.collection.insert_one(data)
            log_event("INFO", "one document saved successfully")
        except Exception as e:
            log_event("ERROR", e)


mongo_instance = Mongodb()