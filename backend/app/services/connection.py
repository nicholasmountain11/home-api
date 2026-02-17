import socket
from typing import Any


class ConnectionService:

    def __init__(self, port: int):
        self.host = "127.0.0.1"  # localhost
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, port))
        self.server.listen()
        print("Listening")

    def message(self) -> str:
        return "Hello from service"

    def handle(self, client: Any):
        """Wait for messages from client. Broadcast all messages, and close connection on client error"""
        print("new thread, waiting for client message")
        while True:
            # try to receive message from client and broadcast to all other clients
            try:
                message = client.recv(1024)
                print(message)
            # if error with client occurs, close connection with client and remove them from the clients list
            except:
                client.close()
                print("connection closed")
                break

    def receive(self):
        """Wait for new connections"""
        while True:
            try:
                client, address = self.server.accept()
                print(f"Connected with {str(address)}")

                message = client.recv(1024).decode("ascii")

                print(f"Received message: {message}!")
            except Exception as e:
                print(e)
                client.close()
