# src/tcp_handler/server.py

import socket
import threading
import json

from metric_collector import MetricCollector

from logger import Log

log = Log("tcp_handler")

class BaseTCP:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        log.debug(f"BaseTCP instance created for {server_host}:{server_port}")

    def connect(self):
        log.debug("Attempting to establish connection...")
        self.socket = socket.create_connection((self.server_host, self.server_port))
        self._handshake()
        log.info("Connection established with handshake.")

    def _handshake(self):
        log.debug("Starting handshake process...")
        self.socket.sendall(b'SYN')
        response = self.socket.recv(1024)
        if response == b'SYN/ACK':
            self.socket.sendall(b'ACK')
            log.debug("Handshake successful.")
        else:
            log.debug(f"Handshake failed. Response: {response}")

    def send(self, message):
        if not self.socket:
            log.error("Not connected to server.")
            return

        message_length = len(message)
        log.debug(f"Preparing to send message of length: {message_length}")

        # Envoi de la taille du message
        self.socket.sendall(str(message_length).encode('utf-8'))
        log.debug("Message length sent.")

        # Signal pour le début du message
        self.socket.sendall(b'STARTMSG')
        log.debug("Sent STARTMSG signal.")

        # Découpage et envoi du message en morceaux de 1024 octets
        for i in range(0, len(message), 1024):
            chunk = message[i:i+1024]
            self.socket.sendall(chunk.encode('utf-8'))
            log.debug(f"Sent message chunk: {chunk}")

        # Signal pour la fin du message
        self.socket.sendall(b'ENDMSG')
        log.debug("Sent ENDMSG signal.")
        log.info("Message sent successfully.")

    def receive(self):
        if not self.socket:
            log.error("Not connected to server.")
            return

        log.debug("Preparing to receive message...")
        # Réception de la taille du message
        message_length_str = self._recv_until(b'STARTMSG')
        message_length = int(message_length_str)
        log.debug(f"Message length received: {message_length}")

        received_data = b''

        # Réception du message en morceaux de 1024 octets
        while len(received_data) < message_length:
            chunk = self.socket.recv(min(1024, message_length - len(received_data)))
            received_data += chunk
            log.debug(f"Received message chunk: {chunk}")

        # Vérifier la fin du message
        end_signal = self.socket.recv(7)
        if end_signal != b'ENDMSG':
            log.error("Message not properly terminated.")
            return None
        log.debug("Received ENDMSG signal.")

        return received_data.decode('utf-8')

    def _recv_until(self, delimiter):
        data = b''
        while not data.endswith(delimiter):
            data += self.socket.recv(1)
        log.debug(f"Received data until delimiter: {data}")
        return data[:-len(delimiter)]

    def close(self):
        if self.socket:
            self.socket.close()
            log.info("Connection closed.")

class TCPClient(BaseTCP):
    def __init__(self, server_host, server_port, harvester_id):
        super().__init__(server_host, server_port)
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

    def connect(self):
        log.debug(f"Connecting to server")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        self.client_socket.sendall(str(self.client_id).encode('utf-8'))
        log.info(f"Connected to server with ID: {self.client_id}")

    def receive_messages(self):
        while True:
            response = self.client_socket.recv(1024).decode('utf-8')
            log.info(f"Server command: {response}")
            if response == "HEARTBEAT":
                self.client_socket.sendall(b'HEARTBEAT')
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
                self.client_socket.sendall(data.encode('utf-8'))
                log.info(f"Info sent")

            elif response.startswith("NMAP"):
               raise NotImplementedError("NMAP is not implemented yet")

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            log.info(f"Connection closed")