# src/tcp_handler/server.py

import json
import socket
import struct
import threading

from logger import Log
from metric_collector import MetricCollector
from nmap_scanner import NMAPHandler

log = Log("tcp_handler")


class TCPClient:
    def __init__(self, server_host, server_port, harvester_id):
        log.debug(f"Initializing TCPClient for {server_host}:{server_port}")
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

    @staticmethod
    def _preprocess_send(message):
        log.debug(f"Preprocessing message")
        message = str(message).encode('utf-8')
        return struct.pack('>I', len(message)) + message

    def connect(self):
        log.debug(f"Connecting to server")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        msg = self._preprocess_send(str(self.client_id))
        self.client_socket.sendall(msg)
        log.info(f"Connected to server with ID: {self.client_id}")

    def _recvall(self, n):
        log.debug(f"Receiving {n} bytes")
        data = bytearray()
        while len(data) < n:
            log.debug(f"Receiving packet, {n - len(data)} bytes remaining")
            packet = self.client_socket.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def _process_recv(self):
        raw_msglen = self._recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self._recvall(msglen)

    def receive_messages(self):
        while True:
            response = self._process_recv()
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
