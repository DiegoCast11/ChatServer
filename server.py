import socket
import threading
import struct

host = '0.0.0.0'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")

clients = []
usernames = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            decoded_message = message.decode('utf-8')
            if decoded_message.startswith("@"):
                recipient_username, private_message = decoded_message.split(' ', 1)
                recipient_index = usernames.index(recipient_username[1:])
                recipient_client = clients[recipient_index]
                sender_username = usernames[clients.index(client)]
                recipient_client.send(f"(Private) {sender_username}: {private_message}".encode('utf-8'))
            elif decoded_message.startswith("/send"):
                receive_file(client,"file.txt")
                print("File received")

            else:
                sender_username = usernames[clients.index(client)]
                message = f"{sender_username}: {decoded_message}".encode('utf-8')
                broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"ChatBot: {username} disconnected".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")

        message = f"ChatBot: {username} joined the chat!".encode("utf-8")
        broadcast(message, client)
        client.send("Connected to server".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

def receive_file_size(client):
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()
    while received_bytes < expected_bytes:
        chunk = client.recv(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)
        filesize = struct.unpack(fmt, stream)[0]
        return filesize

def receive_file(client, filename):
    filesize = receive_file_size(client)
    with open(filename, 'wb') as file:
        received_bytes = 0
        while received_bytes < filesize:
            chunk = client.recv(1024)
            if chunk:
                file.write(chunk)
                received_bytes += len(chunk)


receive_connections()
