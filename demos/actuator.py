import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8002))


def receive():
    while True:
        message = client.recv(1024).decode()
        if message == "":
            raise RuntimeError("connection closed")
        print(f"message received: {message}")


nickname = input("Enter actuator nickname: ")
client.send(nickname.encode("ascii"))
confirmation = client.recv(1024).decode()
if confirmation == "":
    print("socket connection broken")
    client.close()
print(confirmation)

if nickname == confirmation:
    while True:
        try:
            receive()
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
