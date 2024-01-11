import json
from datetime import datetime

import nmap
import psutil

from logger import Log


import platform
import socket
import uuid
import psutil
import requests

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

    @staticmethod
    def get_system_info():
        try:
            info = {}

            # Système d'exploitation, version, et détails du hardware
            info['os'] = platform.system()
            info['os_version'] = platform.version()
            info['processor'] = platform.processor()
            info['architecture'] = platform.machine()
            info['physical_cores'] = psutil.cpu_count(logical=False)
            info['total_memory'] = psutil.virtual_memory().total

            # Uptime
            info['uptime'] = psutil.boot_time()

            # Adresse MAC et IP
            info['mac_address'] = ':'.join(
                ['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
            info['private_ip'] = socket.gethostbyname(socket.gethostname())
            info['public_ip'] = requests.get('https://api.ipify.org').text

            # Espace disque
            disk_partitions = psutil.disk_partitions()
            for partition in disk_partitions:
                usage = psutil.disk_usage(partition.mountpoint)
                info[f"{partition.device} Total"] = usage.total
                info[f"{partition.device} Used"] = usage.used
                info[f"{partition.device} Free"] = usage.free

            # Informations sur la batterie
            if hasattr(psutil, "sensors_battery"):
                battery = psutil.sensors_battery()
                if battery:
                    info['battery_percent'] = battery.percent
                    info['battery_secsleft'] = battery.secsleft
                    info['battery_power_plugged'] = battery.power_plugged

            # Informations sur les processus en cours
            info['active_processes'] = [p.info for p in psutil.process_iter(attrs=['pid', 'name'])]

            # Informations réseau
            net_info = psutil.net_if_addrs()
            for interface_name, interface_addresses in net_info.items():
                for address in interface_addresses:
                    if str(address.family) == 'AddressFamily.AF_INET':
                        info[interface_name + '_IP'] = address.address
                    elif str(address.family) == 'AddressFamily.AF_PACKET':
                        info[interface_name + '_MAC'] = address.address

            # Informations sur les températures (si disponible)
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            info[f"{name}_{entry.label}"] = entry.current

            return info
        except Exception as e:
            return str(e)

