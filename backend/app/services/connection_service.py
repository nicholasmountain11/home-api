import socket
import threading
import queue
from typing import Any
from enums.connection_type import ConnectionType
from models.connection import Connection, Message


class ConnectionService:

    DUPE_MSG = "DUPE"

    def __init__(self, sensor_port: int, actuator_port: int):
        self.registry: dict[str, Connection] = {}
        self.sensor_port = sensor_port
        self.actuator_port = actuator_port
        self.host = "127.0.0.1"  # localhost
        sensor_listener_thread = threading.Thread(
            target=self.accept, args=(ConnectionType.SENSOR,)
        )
        sensor_listener_thread.start()
        print(f"Listening for sensors on port {sensor_port}")
        actuator_listening_thread = threading.Thread(
            target=self.accept, args=(ConnectionType.ACTUATOR,)
        )
        actuator_listening_thread.start()
        print(f"Listening for actuators on port {actuator_port}")

    def handshake(self, client: socket.socket, connection_type: ConnectionType) -> str:
        """Perform confirmation handshake with new connection. Return nickname if success, raise exception if faulure"""
        # receive nickname to identify connection
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
        # add connection to registry
        self.registry[nickname] = Connection(
            nickname=nickname, client=client, connection_type=connection_type
        )
        return nickname

    def handle_sensor(self, client: Any):
        """Wait for messages from client. Broadcast all messages, and close connection on client error"""
        print("new sensor thread, waiting for client message")

        try:
            # receive nickname to identify sensor connection
            nickname = self.handshake(
                client=client, connection_type=ConnectionType.SENSOR
            )
            while True:
                # wait for message
                message = client.recv(1024).decode()
                if message == "":
                    raise RuntimeError("socket connection broken")
                self.registry[nickname].add_to_q(message=message)
                print(message)
        # if error with client occurs, close connection with client
        except:
            client.close()
            self.registry.pop(nickname)
            print("connection closed")

    def handle_actuator(self, client: Any):
        """Send messages to client. Close connection on client error"""
        print("new actuator thread, waiting for messsages to send")

        try:
            # receive nickname to identify actuator connection
            nickname = self.handshake(
                client=client, connection_type=ConnectionType.ACTUATOR
            )
            while True:
                # wait for message to send to client, get() blocks when no message is available
                message: Message = self.registry[nickname].get_from_q()
                message_text = message.message
                sent = client.send(message_text.encode("ascii"))
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                message.event.set()
        # if error with client occurs, close connection with client
        except:
            client.close()
            self.registry.pop(nickname)
            print("connection closed")

    def accept(self, connection_type: ConnectionType):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind to sensor or actuator
        server.bind(
            (
                self.host,
                (
                    self.sensor_port
                    if connection_type is ConnectionType.SENSOR
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
                if connection_type is ConnectionType.SENSOR
                else threading.Thread(target=self.handle_actuator, args=(client,))
            )
            ct.start()

    def get_message(self, nickname: str):
        message = self.registry[nickname].get_from_q()
        print(f"got message: {message}")
        return message

    def send_message(self, nickname: str, message: str):
        sent = self.registry[nickname].add_to_q(message=message)
        print(f"sent returned: {sent}")
        if sent:
            print(f"added message to actuator queue")
        else:
            print("failed to send message")

    def get_sensor_nickname_list(self) -> list[str]:
        nicknames: list[str] = []
        for (
            key,
            value,
        ) in self.registry.items():
            if value.connection_type is ConnectionType.SENSOR:
                nicknames.append(key)
        return nicknames

    def get_actuator_nickname_list(self) -> list[str]:
        nicknames: list[str] = []
        for (
            key,
            value,
        ) in self.registry.items():
            if value.connection_type is ConnectionType.ACTUATOR:
                nicknames.append(key)
        return nicknames

    def message(self) -> str:
        return "Hello from sensor service"
