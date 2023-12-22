import os
from metric_collector import MetricCollector
from db_client import DBClient
from time import sleep

collector_name = os.getenv('COLLECTOR_NAME', "dev")
collection_frequency = int(os.getenv('COLLECTION_FREQUENCY', "5"))
nester_endpoint = os.getenv('NESTER_ENDPOINT', "localhost:8080")

uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
db_name = os.getenv("MONGO_DB_NAME","harvesterDB")
collection_name = "metrics"


metric_collector = MetricCollector(collector_name=collector_name)

def main_loop():
    while True:
        metrics = metric_collector.collect_metrics()
        sleep(collection_frequency)


if __name__ == '__main__':
    
    db_client = DBClient(uri, db_name, collection_name)

    data = {"sample_key": "sample_value"}

    db_client.insert_data(data)

    db_client.close()
    main_loop()
