import json
from datetime import datetime

import nmap
import psutil

from logger import Log

log = Log("collector")


class MetricCollector:
    def __init__(self, collector_name):
        log.debug("Initializing MetricCollector")
        self.collector_name = collector_name
        self.nm = nmap.PortScanner()
        log.debug("MetricCollector initialized")

    def collect_cpu_metrics(self):
        log.debug("Collecting CPU metrics")
        cpu_usage = psutil.cpu_percent(interval=1)
        cores = psutil.cpu_count()
        log.debug("CPU metrics collected")
        return {"usage": f"{cpu_usage}%", "cores": cores, "temperature": "N/A"}

    def collect_memory_metrics(self):
        log.debug("Collecting memory metrics")
        memory = psutil.virtual_memory()
        log.debug("Memory metrics collected")
        return {
            "total": f"{memory.total / (1024 ** 3):.2f}GB",
            "used": f"{memory.used / (1024 ** 3):.2f}GB",
            "free": f"{memory.available / (1024 ** 3):.2f}GB"
        }

    def collect_disk_metrics(self):
        log.debug("Collecting disk metrics")
        disks = []
        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append({
                "diskName": partition.device,
                "capacity": f"{usage.total / (1024 ** 3):.2f}GB",
                "used": f"{usage.used / (1024 ** 3):.2f}GB",
                "free": f"{usage.free / (1024 ** 3):.2f}GB"
            })
        log.debug("Disk metrics collected")
        return disks

    def run_nmap_scan(self, nmap_input):
        log.debug("Running Nmap scan")
        self.nm.scan(hosts=nmap_input, arguments='-v')
        log.info("Nmap scan completed")
        return self.nm.command_line(), str(self.nm.all_hosts())

    def generate_json(self, nmap_input):
        log.debug("Generating JSON")
        nmap_command, nmap_results = self.run_nmap_scan(nmap_input)
        data = {
            "collectorName": self.collector_name,
            "timeOfCollect": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "metrics": {
                "cpu": self.collect_cpu_metrics(),
                "memory": self.collect_memory_metrics(),
                "disk": self.collect_disk_metrics()
            },
            "nmapScanInput": nmap_command,
            "nmapScanOutput": nmap_results
        }
        log.info("JSON generated")
        return json.dumps(data, indent=2)
