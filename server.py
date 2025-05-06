import datetime
import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
clients = []
clients_mutex = threading.Lock()


def handle_client(socket):
    while True:
        data = socket.recv(1024).decode()
        with clients_mutex:
            for client_socket in clients:
                if client_socket == socket:
                    print(f"{datetime.datetime.now()} - {data}")
                    continue

                message = f"{datetime.datetime.now()} - {data}"
                client_socket.sendall(message.encode())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        socket, address = s.accept()
        print(f"{address} connected")

        with clients_mutex:
            clients.append(socket)

        client = threading.Thread(target=handle_client, args=(socket,))
        client.start()
