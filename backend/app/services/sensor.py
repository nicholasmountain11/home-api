import socket
import threading
import queue
from typing import Any


class SensorService:

    DUPE_MSG = "DUPE"

    def __init__(self, port: int):
        self.registry = {}
        self.port = port
        self.host = "127.0.0.1"  # localhost
        listener_thread = threading.Thread(target=self.accept)
        listener_thread.start()
        print(f"Listening on port {port}")

    def handle(self, client: Any):
        """Wait for messages from client. Broadcast all messages, and close connection on client error"""
        print("new thread, waiting for client message")
        q = queue.Queue(maxsize=5)

        try:
            # receive nickname to identify sensor connection
            nickname = client.recv(1024).decode()
            print(nickname)
            if nickname == "":
                raise RuntimeError("failed to get nickname")
            if nickname in self.registry:
                print("duplicate nickname")
                client.send(self.DUPE_MSG.encode("ascii"))
                raise RuntimeError("duplicate nickname")
            # send confirmation of nickname
            sent = client.send(nickname.encode("ascii"))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            # add sensor to registry
            self.registry[nickname] = (client, q)
            while True:
                # wait for message
                message = client.recv(1024).decode()
                if message == "":
                    raise RuntimeError("socket connection broken")
                q.put(message)
                print(message)
        # if error with client occurs, close connection with client
        except:
            client.close()
            self.registry.pop(nickname)
            print("connection closed")

    def accept(self) -> str:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print("Listening")
        while True:
            client, address = server.accept()
            print(f"Connected with {str(address)}")
            ct = threading.Thread(target=self.handle, args=(client,))
            ct.start()

    def get_message(self, nickname: str):
        message = self.registry[nickname][1].get()
        print(f"got message: {message}")
        return message

    def message(self) -> str:
        return "Hello from sensor service"

    # def receive(self):
    #     """Wait for new connections"""
    #     while True:
    #         try:
    #             client, address = self.server.accept()
    #             print(f"Connected with {str(address)}")

    #             nickname = client.recv(1024).decode("ascii")

    #             print(f"Sensor nickname is: {nickname}!")

    #             thread = threading.Thread(target=self.handle, args=(client,))
    #             thread.start()
    #             return f"Listening on port {self.port}"

    #         except Exception as e:
    #             print(e)
    #             client.close()
