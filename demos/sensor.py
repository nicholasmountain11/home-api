import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8001))


def write():
    while True:
        message = input("Enter demo message: ")
        client.send(message.encode("ascii"))


while True:
    try:
        write()
    except Exception as e:
        print(e)
        client.close()
        break
