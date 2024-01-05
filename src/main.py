import os
from metric_collector import MetricCollector
from db_client import DBClient
from tcp_handler import TCPServer
from time import sleep

collector_name = os.getenv('COLLECTOR_NAME', "dev")
collection_frequency = int(os.getenv('COLLECTION_FREQUENCY', "5"))
nester_endpoint = os.getenv('NESTER_ENDPOINT', "localhost:8080")

uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
db_name = os.getenv("MONGO_DB_NAME","harvesterDB")
collection_name = "metrics"

tcp_port = int(os.getenv("TCP_PORT", "5000"))


metric_collector = MetricCollector(collector_name= collector_name + "__" + str(tcp_port))
db_client = DBClient(uri, db_name, collection_name)

def main_loop():
    while True:
        metrics = metric_collector.collect_metrics()
        db_client.insert_data(metrics)
        sleep(collection_frequency)


if __name__ == '__main__':
    tcp_server = TCPServer(host='0.0.0.0', port=tcp_port)
    tcp_server.start()

