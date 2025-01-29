import socket
import threading


def recive(client: socket.socket):
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "INSERT USERNAME":
                client.send(username.encode())
            else:
                print(message)
        except ConnectionAbortedError as e:
            print(f"❌ Connection aborted: {e}")
            client.close()
            break
        except OSError as e:
            print(f"❌ An error occurred while receiving a message: {e}")
            client.close()
            break


def write(client: socket.socket):
    while True:
        try:
            message = f"[{username}]$ {input('')}"
            client.send(message.encode())
        except ConnectionAbortedError as e:
            print(f"❌ Connection aborted: {e}")
            client.close()
            break
        except OSError as e:
            print(f"❌ An error occurred while sending a message: {e}")
            client.close()
            break


if __name__ == "__main__":
    HOST = input("🔗 Insert the IP or URL of the server to connect to: ")
    PORT = int(input("🚪 Insert the TCP PORT of the server to connect to: "))

    username = input("🧑 Choose a username: ")
    while not username:
        username = input("🧑 Choose a username: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    recive_thread = threading.Thread(target=recive, args=(client,))
    recive_thread.start()

    write_thread = threading.Thread(target=write, args=(client,))
    write_thread.start()
