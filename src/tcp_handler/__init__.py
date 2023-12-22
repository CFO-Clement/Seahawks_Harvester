"""
# main.py

from tcp_handler.server import TCPServer

def main_loop():
    while True:
        # Your main application logic here
        # ...

if __name__ == "__main__":
    tcp_server = TCPServer(host='0.0.0.0', port=5000)
    tcp_server.start()

    main_loop()

"""