import socket, threading, queue
from enums.connection_type import ConnectionType


class Message:
    def __init__(self, message: str, event: threading.Event | None = None):
        self.message = message
        self.event = event


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

    def add_to_q(self, message: str) -> bool:
        send_event = threading.Event()
        print("after send event")
        message_with_event = Message(message=message, event=send_event)
        print("after message with event")
        self.q.put(message_with_event)
        print("after put")
        return send_event.wait(timeout=5)
