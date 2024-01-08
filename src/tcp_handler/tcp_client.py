# src/tcp_handler/server.py

import socket
import threading

from logger import Log

log = Log("tcp_handler")

class TCPClient:
    def __init__(self, server_host, server_port):
        log.debug(f"Initializing TCPClient for {server_host}:{server_port}")
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = None
        log.debug(f"TCPClient initialized")

    def connect(self):
        log.debug(f"Connecting to server")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        self.client_id = self.client_socket.recv(1024).decode('utf-8')
        log.info(f"Connected to server with ID: {self.client_id}")

    def receive_messages(self):
        while True:
            response = self.client_socket.recv(1024).decode('utf-8')
            log.info(f"Server command: {response}")

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            log.info(f"Connection closed")