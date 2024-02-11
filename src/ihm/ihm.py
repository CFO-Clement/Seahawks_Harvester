import threading
import time
import tkinter as tk

import psutil
from logger import Log

log = Log("ihm")


class SystemMetricsDashboard(tk.Tk):
    """
    System Metrics Dashboard class, responsible for displaying system metrics
    """

    def __init__(self):
        """
        Initialize the SystemMetricsDashboard
        """
        log.debug("Initializing SystemMetricsDashboard")
        super().__init__()
        self.title("System Metrics Dashboard")
        self.geometry("400x300")

        self.cpu_label = tk.Label(self, text="CPU Usage:")
        self.cpu_label.pack()

        self.ram_label = tk.Label(self, text="RAM Usage:")
        self.ram_label.pack()

        self.disk_label = tk.Label(self, text="Disk Usage:")
        self.disk_label.pack()

        # Variables pour stocker les métriques
        self.metrics = {
            "cpu_percent": 0,
            "ram_percent": 0,
            "disk_percent": 0
        }

        self.update_metrics_thread = None
        self.running = threading.Event()
        self.running.set()

    def fetch_metrics(self):
        """
        Fetch metrics from the system
        :return: None
        """
        log.debug("Starting metrics fetching")
        while self.running.is_set():
            # Mise à jour des métriques dans un dictionnaire
            self.metrics["cpu_percent"] = psutil.cpu_percent()
            self.metrics["ram_percent"] = psutil.virtual_memory().percent
            self.metrics["disk_percent"] = psutil.disk_usage('/').percent
            time.sleep(1)

    def update_metrics_ui(self, stop_event):
        """
        Update the UI with the metrics
        :param stop_event: The stop event
        :return: None
        """
        if stop_event.is_set():
            log.critical("Critical error detected")
            log.info("Stopping UI")
            self.stop_dashboard()
            log.info("UI stopped")

            raise SystemExit("Critical error have been raised")

        self.cpu_label.config(text=f"CPU Usage: {self.metrics['cpu_percent']}%")
        self.ram_label.config(text=f"RAM Usage: {self.metrics['ram_percent']}%")
        self.disk_label.config(text=f"Disk Usage: {self.metrics['disk_percent']}%")
        if self.running.is_set():
            self.after(1000, lambda: self.update_metrics_ui(stop_event))

    def start_dashboard(self, stop_event):
        """
        Start the SystemMetricsDashboard
        :param stop_event: The stop event
        :return: None
        """
        log.debug("Starting UI")
        if self.update_metrics_thread is None or not self.update_metrics_thread.is_alive():
            self.update_metrics_thread = threading.Thread(target=self.fetch_metrics, daemon=True)
            self.update_metrics_thread.start()
            self.update_metrics_ui(stop_event)

    def stop_dashboard(self):
        """
        Stop the SystemMetricsDashboard
        :return: None
        """
        log.info("Cleaning UI")
        self.running.clear()
        if self.update_metrics_thread:
            self.update_metrics_thread.join()
        log.info("all thread are quiting")
        self.quit()
