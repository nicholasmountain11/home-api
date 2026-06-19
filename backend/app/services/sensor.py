import socket
import threading
from typing import Any


class SensorService:

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
        while True:
            # try to receive message from client
            try:
                message = client.recv(1024)
                if message == b"":
                    raise RuntimeError("socket connection broken")
                print(message)
            # if error with client occurs, close connection with client
            except:
                client.close()
                print("connection closed")
                break

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
