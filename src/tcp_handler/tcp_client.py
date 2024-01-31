# src/tcp_handler/server.py

import json
import socket
import threading

from logger import Log
from metric_collector import MetricCollector
from nmap_scanner import NMAPHandler
from .tcp_base import TCPBase

log = Log("tcp_handler")


class TCPClient(TCPBase):
    def __init__(self, server_host, server_port, harvester_id):
        log.debug(f"Initializing TCPClient for {server_host}:{server_port}")
        super().__init__()
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = None
        self.client_id = harvester_id
        self.thread = None
        log.debug(f"TCPClient initialized")

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        self.connect()
        self.receive_messages()

    def connect(self):
        log.debug(f"Connecting to server")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        msg = self._preprocess_send(str(self.client_id))
        self.client_socket.sendall(msg)
        log.info(f"Connected to server with ID: {self.client_id}")

    def receive_messages(self):
        while True:
            response = self._process_recv(self.client_socket)
            log.debug(f"Raw server command: {response}")
            response = response.decode('utf-8')
            log.info(f"Server command: {response}")
            if response == "HEARTBEAT":
                self.client_socket.sendall(self._preprocess_send('HEARTBEAT'))
            elif response == "CLOSE":
                self.client_socket.close()
                log.info(f"Connection closed")
                break
            elif response == "KILL":
                self.client_socket.close()
                log.info(f"Connection closed")
                exit(0)
            elif response == "INFO":
                log.info(f"Sending info to server")
                data = json.dumps(MetricCollector(self.client_id).get_system_info())
                self.client_socket.sendall(self._preprocess_send(data))
                log.info(f"Info sent")

            elif response.startswith("NMAP"):
                log.info(f"Handling NMAP command from server")
                handler = NMAPHandler()
                try:
                    response = handler.handle_command(response)
                except NotImplementedError as e:
                    response = {
                        "status": "error",
                        "message": str(e)
                    }
                self.client_socket.sendall(self._preprocess_send(response))
                log.info(f"NMAP result sent")

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            log.info(f"Connection closed")
