import os

from time import sleep

from ihm import SystemMetricsDashboard
from logger import Log
from metric_collector import MetricCollector
from tcp_handler import TCPClient

log = Log("main")

harvester_id = os.getenv('HARVESTER_NAME', "dev")
harvester_frequency = int(os.getenv('HARVESTER_FREQUENCY', "1000"))
nester_endpoint = os.getenv('NESTER_ENDPOINT', "localhost")
nester_port = int(os.getenv('NESTER_PORT', "5001"))

uri = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
db_name = os.getenv("MONGO_DB_NAME", "mongo")
collection_name = "metrics"

metric_collector = MetricCollector(collector_name=harvester_id + "__" + str(nester_port))
# db_client = DBClient(uri, db_name, collection_name)
app = SystemMetricsDashboard()


def main_loop():
    while True:
        metrics = metric_collector.collect_metrics()
        # db_client.insert_data(metrics)
        sleep(harvester_frequency)


if __name__ == '__main__':
    log.info("Starting TCP server")
    client = TCPClient(nester_endpoint, nester_port, harvester_id)

    log.info("Connecting to TCP server")
    client.start()

    log.info("Starting dashboard app")
    app.start_dashboard()
    app.mainloop()

    log.info("Harvester initialized, starting main loop")
    main_loop()
