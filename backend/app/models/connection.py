import socket, threading, queue


class Connection:

    nickname: str
    client: socket.socket
    q: queue.Queue

    def __init__(self, nickname: str, client: socket.socket):
        self.nickname = nickname
        self.client = client
        self.q = queue.Queue()

    def get_from_q(self):
        return self.q.get()

    def add_to_q(self, message: str):
        self.q.put(message)
