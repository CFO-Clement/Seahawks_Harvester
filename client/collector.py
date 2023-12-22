import json
import psutil
import nmap
from datetime import datetime

class MetrixCollector:
    def __init__(self, collector_name):
        self.collector_name = collector_name
        self.nm = nmap.PortScanner()

    def collect_cpu_metrics(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        cores = psutil.cpu_count()
        return {"usage": f"{cpu_usage}%", "cores": cores, "temperature": "N/A"}

    def collect_memory_metrics(self):
        memory = psutil.virtual_memory()
        return {
            "total": f"{memory.total / (1024 ** 3):.2f}GB",
            "used": f"{memory.used / (1024 ** 3):.2f}GB",
            "free": f"{memory.available / (1024 ** 3):.2f}GB"
        }

    def collect_disk_metrics(self):
        disks = []
        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append({
                "diskName": partition.device,
                "capacity": f"{usage.total / (1024 ** 3):.2f}GB",
                "used": f"{usage.used / (1024 ** 3):.2f}GB",
                "free": f"{usage.free / (1024 ** 3):.2f}GB"
            })
        return disks

    def run_nmap_scan(self, nmap_input):
        self.nm.scan(hosts=nmap_input, arguments='-v')
        return self.nm.command_line(), str(self.nm.all_hosts())

    def generate_json(self, nmap_input):
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
        return json.dumps(data, indent=2)
