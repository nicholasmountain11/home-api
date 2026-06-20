import socket, threading, queue
from enums.connection_type import ConnectionType


class Connection:

    nickname: str
    client: socket.socket
    q: queue.Queue
    connection_type: ConnectionType

    def __init__(
        self, nickname: str, client: socket.socket, connection_type: ConnectionType
    ):
        self.nickname = nickname
        self.client = client
        self.q = queue.Queue()
        self.connection_type = connection_type

    def get_from_q(self):
        return self.q.get()

    def add_to_q(self, message: str):
        self.q.put(message)
