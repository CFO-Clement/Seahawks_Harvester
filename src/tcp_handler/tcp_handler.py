# src/tcp_handler/server.py

import socket
import threading

from logger import Log

log = Log("tcp_handler")


class TCPServer:
    def __init__(self, host='0.0.0.0', port=5000):
        log.debug(f"Initializing TCPServer on {host}:{port}")
        self.host = host
        self.port = port
        self.server_thread = None
        log.debug(f"TCPServer initialized")

    def start(self):
        # Start the TCP server in a separate thread
        log.debug(f"Starting TCPServer")
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()
        log.info(f"TCPServer started")

    def _run_server(self):
        # Main loop of the TCP server
        log.debug(f"Starting TCP server loop")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.host, self.port))
            server.listen(5)
            log.info(f"TCP server listening on {self.host}:{self.port}")

            while True:
                client_sock, address = server.accept()
                log.info(f"New connection from {address[0]}:{address[1]}")
                client_handler = threading.Thread(target=self.handle_client_connection, args=(client_sock,))
                client_handler.start()

    def handle_client_connection(self, client_socket):
        # Handle an individual client connection
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                log.info(f"Received message: {message}")
                response = self.process_command(message)
                client_socket.sendall(response.encode('utf-8'))
        finally:
            log.debug(f"Closing connection")
            client_socket.close()

    def process_command(self, command):
        # Process the received command
        log.info(f"Processing command: {command}")
        if command == "Are you alive?":
            log.info(f"Command is 'Are you alive?'")
            return "Yes, I'm alive"
        elif command.startswith("run_nmap"):
            log.info(f"Command is 'run_nmap'")
            nmap_command = command.split(" ", 1)[1]
            raise NotImplementedError("run_nmap is not implemented yet")
        else:
            log.info(f"Command is unknown")
            return "Unknown command"
