import socket
import sys
import os
from dotenv import load_dotenv

load_dotenv()

ip: str

if len(sys.argv) > 1 and sys.argv[1] == "network":
    ip = os.environ["LOCAL_IP"]
else:
    ip = os.environ["LOCAL_HOST"]


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.1.244", 8001))


def write():
    while True:
        message = input("Enter demo message: ")
        client.send(message.encode("ascii"))


nickname = input("Enter sensor nickname: ")
client.send(nickname.encode("ascii"))
confirmation = client.recv(1024).decode()
print(confirmation)

if nickname == confirmation:
    while True:
        try:
            write()
        except Exception as e:
            print(e)
            client.close()
            break
elif confirmation == "DUPE":
    print("that nickname is already in use")
    client.close()

else:
    print("incorrect nickname confirmation")
    client.close()
