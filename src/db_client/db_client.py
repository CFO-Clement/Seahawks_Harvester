# db_client/client.py

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class DBClient:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        try:
            self.client.admin.command('ismaster')
        except ConnectionFailure:
            print("MongoDB connection failed. Please check your connection settings.")
            exit(1)

    def insert_data(self, data):
        try:
            self.collection.insert_one(data)
        except Exception as e:
            print(f"An error occurred while inserting data: {e}")

    def close(self):
        self.client.close()
