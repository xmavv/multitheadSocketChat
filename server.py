import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
clients = []

def handle_client(socket):
    while True:
        data = socket.recv(1024)
        for client in clients:
            client.sendall(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        socket, address = s.accept()
        clients.append(socket)

        print(f"client {address} connected")

        client = threading.Thread(target=handle_client, args=(socket,))
        client.start()
