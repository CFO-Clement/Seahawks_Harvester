# db_client/client.py

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from logger import Log

log = Log("db_client")


class DBClient:
    def __init__(self, uri, db_name, collection_name):
        log.debug(f"Connecting to MongoDB at {uri}")
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        try:
            self.client.admin.command('ismaster')
            log.info(f"Connected to MongoDB at {uri}")
        except ConnectionFailure:
            log.error(f"Could not connect to MongoDB at {uri}")
            exit(1)

    def insert_data(self, data):
        try:
            log.debug(f"Inserting data")
            self.collection.insert_one(data)
            log.debug(f"Data inserted")
        except Exception as e:
            log.error(f"An error occurred while inserting data: {e}")

    def close(self):
        log.debug(f"Closing MongoDB connection")
        self.client.close()
        log.info(f"MongoDB connection closed")
