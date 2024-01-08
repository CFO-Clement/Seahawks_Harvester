from metric_collector import MetricCollector
from db_client import DBClient
from tcp_handler import TCPServer
from ihm import SystemMetricsDashboard
from time import sleep
import os

collector_name = os.getenv('COLLECTOR_NAME', "dev")
collection_frequency = int(os.getenv('COLLECTION_FREQUENCY', "5"))
nester_endpoint = os.getenv('NESTER_ENDPOINT', "localhost:8080")

uri = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
db_name = os.getenv("MONGO_DB_NAME","mongo")
collection_name = "metrics"

tcp_port = int(os.getenv("TCP_PORT", "5000"))


metric_collector = MetricCollector(collector_name=collector_name + "__" + str(tcp_port))
db_client = DBClient(uri, db_name, collection_name)
app = SystemMetricsDashboard()

def main_loop():
    while True:
        metrics = metric_collector.collect_metrics()
        db_client.insert_data(metrics)
        sleep(collection_frequency)


if __name__ == '__main__':
    tcp_server = TCPServer(host=nester_endpoint, port=tcp_port)
    tcp_server.start()
    app.start_dashboard()
    app.mainloop()

