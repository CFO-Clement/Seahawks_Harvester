import os
import threading

from dotenv import load_dotenv

from ihm import SystemMetricsDashboard
from logger import Log
from tcp_handler import TCPClient

log = Log("main")

log.info("Loading environment")
script_dir = os.path.dirname(__file__)
log.debug(f"script_dir: {script_dir}")
env_path = os.path.join(script_dir, '../config.env')
log.debug(f"env_path: {env_path}")
load_dotenv(env_path)

harvester_id = os.getenv('HARVESTER_NAME')

if harvester_id:
    log.debug(f"env successfully loaded")
else:
    log.error(f"env not loaded")
    raise EnvironmentError("env not loaded")

harvester_frequency = int(os.getenv('HARVESTER_FREQUENCY'))
nester_endpoint = os.getenv('NESTER_ENDPOINT')
nester_port = int(os.getenv('NESTER_PORT'))

if __name__ == '__main__':
    stop_event = threading.Event()

    log.info("Starting TCP server")
    client = TCPClient(nester_endpoint, nester_port, harvester_id, stop_event)

    log.info("Connecting to TCP server")
    client.start()

    log.info("Starting dashboard app")
    app = SystemMetricsDashboard()
    app.start_dashboard(stop_event)
    app.mainloop()
