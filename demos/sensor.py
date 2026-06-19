import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8001))


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

else:
    print("incorrect nickname confirmation")
    client.close()
