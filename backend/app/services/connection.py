import socket
import threading
import queue
from typing import Any
from enum import Enum, auto


class Connection_Type(Enum):
    SENSOR = auto()
    ACTUATOR = auto()


class ConnectionService:

    DUPE_MSG = "DUPE"

    def __init__(self, sensor_port: int, actuator_port: int):
        self.registry = {}
        self.actuator_registry = {}
        self.sensor_port = sensor_port
        self.actuator_port = actuator_port
        self.host = "127.0.0.1"  # localhost
        sensor_listener_thread = threading.Thread(
            target=self.accept, args=(Connection_Type.SENSOR,)
        )
        sensor_listener_thread.start()
        print(f"Listening for sensors on port {sensor_port}")
        actuator_listening_thread = threading.Thread(
            target=self.accept, args=(Connection_Type.ACTUATOR,)
        )
        actuator_listening_thread.start()
        print(f"Listening for actuators on port {actuator_port}")

    def handle_sensor(self, client: Any):
        """Wait for messages from client. Broadcast all messages, and close connection on client error"""
        print("new sensor thread, waiting for client message")
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

    def handle_actuator(self, client: Any):
        """Send messages to client. Close connection on client error"""
        print("new actuator thread, waiting for messsages to send")
        q = queue.Queue(maxsize=5)

        try:
            # receive nickname to identify actuatory connection
            nickname = client.recv(1024).decode()
            print(nickname)
            if nickname == "":
                raise RuntimeError("failed to get nickname")
            if nickname in self.actuator_registry:
                print("duplicate nickname")
                client.send(self.DUPE_MSG.encode("ascii"))
                raise RuntimeError("duplicate nickname")
            # send confirmation of nickname
            sent = client.send(nickname.encode("ascii"))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            # add actuator to registry
            self.actuator_registry[nickname] = (client, q)
            while True:
                # wait for message to send to client, get() blocks when no message is available
                message = self.actuator_registry[nickname][1].get()
                sent = client.send(message.encode("ascii"))
                if sent == 0:
                    raise RuntimeError("socket connection broken")
        except:
            client.close()
            self.registry.pop(nickname)
            print("connection closed")

    def accept(self, connection_type: Connection_Type):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind to sensor or actuator
        server.bind(
            (
                self.host,
                (
                    self.sensor_port
                    if connection_type is Connection_Type.SENSOR
                    else self.actuator_port
                ),
            )
        )
        server.listen(5)
        print("Listening")
        while True:
            client, address = server.accept()
            print(f"Connected with {str(address)}")
            # create thread in correct handle function based on connection type
            ct = (
                threading.Thread(target=self.handle_sensor, args=(client,))
                if connection_type is Connection_Type.SENSOR
                else threading.Thread(target=self.handle_actuator, args=(client,))
            )
            ct.start()

    def get_message(self, nickname: str):
        message = self.registry[nickname][1].get()
        print(f"got message: {message}")
        return message

    def send_message(self, nickname: str, message: str):
        self.actuator_registry[nickname][1].put(message)
        print(f"added message to actuator queue")

    def message(self) -> str:
        return "Hello from sensor service"
