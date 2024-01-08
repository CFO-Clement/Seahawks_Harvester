import tkinter as tk
import psutil
import threading

class SystemMetricsDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("System Metrics Dashboard")
        self.geometry("400x300")

        self.cpu_label = tk.Label(self, text="CPU Usage:")
        self.cpu_label.pack()

        self.ram_label = tk.Label(self, text="RAM Usage:")
        self.ram_label.pack()

        self.disk_label = tk.Label(self, text="Disk Usage:")
        self.disk_label.pack()

    def update_metrics(self):
        while True:
            cpu_percent = psutil.cpu_percent()
            ram_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent

            self.cpu_label.config(text=f"CPU Usage: {cpu_percent}%")
            self.ram_label.config(text=f"RAM Usage: {ram_percent}%")
            self.disk_label.config(text=f"Disk Usage: {disk_percent}%")

            self.update()
            time.sleep(1)

    def start_dashboard(self):
        dashboard_thread = threading.Thread(target=self.update_metrics)
        dashboard_thread.daemon = True
        dashboard_thread.start()
