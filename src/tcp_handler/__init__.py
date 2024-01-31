"""
if __name__ == "__main__":
    client = TCPClient('127.0.0.1', 5000)
    client.connect()
"""
from .tcp_client import TCPClient
from .tcp_base import TCPBase
