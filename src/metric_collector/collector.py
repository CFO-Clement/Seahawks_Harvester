import json
import platform
import socket
import uuid
from datetime import datetime

import nmap
import psutil
from logger import Log

log = Log("collector")


class MetricCollector:
    """
    Metric Collector class, responsible for collecting system metrics
    """

    def __init__(self, collector_name):
        """
        Initialize the MetricCollector
        :param collector_name: The name of the collector
        """
        log.debug("Initializing MetricCollector")
        self.collector_name = collector_name
        self.nm = nmap.PortScanner()
        log.debug("MetricCollector initialized")

    def collect_cpu_metrics(self):
        """
        Collect CPU metrics
        :return: CPU metrics
        """
        log.debug("Collecting CPU metrics")
        cpu_usage = psutil.cpu_percent(interval=1)
        cores = psutil.cpu_count()
        log.debug("CPU metrics collected")
        return {"usage": f"{cpu_usage}%", "cores": cores, "temperature": "N/A"}

    def collect_memory_metrics(self):
        """
        Collect memory metrics
        :return: Memory metrics
        """
        log.debug("Collecting memory metrics")
        memory = psutil.virtual_memory()
        log.debug("Memory metrics collected")
        return {
            "total": f"{memory.total / (1024 ** 3):.2f}GB",
            "used": f"{memory.used / (1024 ** 3):.2f}GB",
            "free": f"{memory.available / (1024 ** 3):.2f}GB"
        }

    def collect_disk_metrics(self):
        """
        Collect disk metrics
        :return: Disk metrics
        """
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

    def generate_json(self):
        """
        Generate JSON with the collected metrics
        :return: JSON with the collected metrics
        """
        log.debug("Generating JSON")
        data = {
            "collectorName": self.collector_name,
            "timeOfCollect": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "metrics": {
                "cpu": self.collect_cpu_metrics(),
                "memory": self.collect_memory_metrics(),
                "disk": self.collect_disk_metrics()
            },
        }
        log.info("JSON generated")
        return json.dumps(data, indent=2)

    @staticmethod
    def get_system_info():
        """
        Get system information
        :return: System information
        """
        log.debug("Getting system info")
        try:
            info = {}
            # Système d'exploitation, version, et détails du hardware
            log.debug("Getting OS info")
            info['os'] = platform.system()
            info['os_version'] = platform.version()
            info['processor'] = platform.processor()
            info['architecture'] = platform.machine()
            info['physical_cores'] = psutil.cpu_count(logical=False)
            info['total_memory'] = psutil.virtual_memory().total

            # Uptime
            log.debug("Getting uptime")
            info['uptime'] = psutil.boot_time()

            # Adresse MAC et IP
            log.debug("Getting MAC and IP addresses")
            info['mac_address'] = ':'.join(
                ['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
            info['private_ip'] = socket.gethostbyname(socket.gethostname())
            info['public_ip'] = "my ip"  # requests.get('https://api.ipify.org').text

            # Espace disque
            log.debug("Getting disk space")
            disk_partitions = psutil.disk_partitions()
            for partition in disk_partitions:
                usage = psutil.disk_usage(partition.mountpoint)
                info[f"{partition.device} Total"] = usage.total
                info[f"{partition.device} Used"] = usage.used
                info[f"{partition.device} Free"] = usage.free

            # Informations sur la batterie
            log.debug("Getting battery info")
            if hasattr(psutil, "sensors_battery"):
                battery = psutil.sensors_battery()
                if battery:
                    info['battery_percent'] = battery.percent
                    info['battery_secsleft'] = battery.secsleft
                    info['battery_power_plugged'] = battery.power_plugged

            # Informations sur les processus en cours
            log.debug("Getting running processes")
            processes = []
            for process in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']):
                processes.append(process.info)

            processes.sort(key=lambda x: x['memory_percent'] if x['memory_percent'] is not None else 0, reverse=True)
            info['processes'] = processes[:10]

            # Informations réseau
            log.debug("Getting network info")
            net_info = psutil.net_if_addrs()
            for interface_name, interface_addresses in net_info.items():
                for address in interface_addresses:
                    if str(address.family) == 'AddressFamily.AF_INET':
                        info[interface_name + '_IP'] = address.address
                    elif str(address.family) == 'AddressFamily.AF_PACKET':
                        info[interface_name + '_MAC'] = address.address

            # Informations sur les températures (si disponible)
            log.debug("Getting temperature info")
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            info[f"{name}_{entry.label}"] = entry.current
            log.info("System info collected")
            open('info.json', 'w').write(json.dumps(info, indent=2))
            return info
        except Exception as e:
            log.error(f"Error while getting system info: {e}")
            return str(e)
