import os

collector_name = os.getenv('COLLECTOR_NAME', "dev")
collection_frequency = os.getenv('COLLECTION_FREQUENCY', "5")
nester_endpoint = os.getenv('NESTER_ENDPOINT', "localhost:8080")





