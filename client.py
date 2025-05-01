import socket
import threading

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def handle_send(s):
    while True:
        message = input()
        s.sendall(message.encode())

def handle_receive(s):
    while True:
        data = s.recv(1024)
        if not data:
            print("Połączenie zostało zamknięte przez serwer.")
            break
        print(data.decode())

#cant use with because since with statement is done, the variable s is deleted from memory or close itself immediately
def __main__():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    send_thread = threading.Thread(target=handle_send, args=(s,))
    receive_thread = threading.Thread(target=handle_receive, args=(s,))
    receive_thread.start()
    send_thread.start()

__main__()