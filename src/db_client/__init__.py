# db_client/__init__.py

"""
from db_client import DBClient

uri = "mongodb://localhost:27017/"
db_name = "harvesterDB"
collection_name = "metrics"

db_client = DBClient(uri, db_name, collection_name)

data = {"sample_key": "sample_value"}

db_client.insert_data(data)

db_client.close()
"""


from .db_client import DBClient
