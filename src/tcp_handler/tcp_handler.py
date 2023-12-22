# src/tcp_handler/server.py

import socket
import threading

class TCPServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server_thread = None

    def start(self):
        # Start the TCP server in a separate thread
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()

    def _run_server(self):
        # Main loop of the TCP server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.host, self.port))
            server.listen(5)
            print(f"TCP Server listening on {self.host}:{self.port}")

            while True:
                client_sock, address = server.accept()
                print(f"Connection from {address}")
                client_handler = threading.Thread(target=self.handle_client_connection, args=(client_sock,))
                client_handler.start()

    def handle_client_connection(self, client_socket):
        # Handle an individual client connection
        try:
            while True:
                message = client_socke∏t.recv(1024).decode('utf-8')
                if not message:
                    break

                response = self.process_command(message)
                client_socket.sendall(response.encode('utf-8'))
        finally:
            client_socket.close()

    def process_command(self, command):
        # Process the received command
        if command == "Are you alive?":
            return "Yes, I'm alive"
        elif command.startswith("run_nmap"):
            nmap_command = command.split(" ", 1)[1]
            raise NotImplementedError("run_nmap is not implemented yet")
        else:
            return "Unknown command"
