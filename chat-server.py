import threading
import socket
from typing import ByteString

HOST = "0.0.0.0"
PORT = 9999

clients = []
usernames = []


def broadcast(message: ByteString):
    for client in clients:
        client.send(message)


def handle_client_message(client: socket.socket):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message=message)
        except:
            index = clients.index(client)
            clients.remove(client)
            username = usernames[index]

            broadcast(f"{username} left the chat!".encode())
            usernames.remove(username)
            client.close()
            break


def accept_client_connection(server_socket: socket.socket):
    while True:
        # accept all the connection requests of all the clients
        client, addr = server_socket.accept()

        try:
            print(f"🔌 Connected by {addr}")

            # ask the client to insert his username
            client.send("INSERT USERNAME".encode())
            username = client.recv(1024).decode()
            # saves client connection and username
            usernames.append(username)
            clients.append(client)

            print(f"👤 Username of the client is {username}")
            broadcast(f"{username} joined the chat!".encode())
            client.send("Connected to the server!".encode())

            thread = threading.Thread(target=handle_client_message, args=(client,))
            thread.start()
        except:
            client.close()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # bind the socket to a port and start listening for connections
        s.bind((HOST, PORT))
        s.listen()
        print(f"🀄 Server is listening on port {PORT}")

        accept_client_connection(server_socket=s)
