from pymongo import MongoClient
from config import Config


class Connection:
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.DATABASE_NAME]

    def get_collection(self, collection_name):
        return self.db[collection_name]
