import socket
import threading

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
                file_name = decoded_message.split(' ')[1]
                client.send(f"Sending file '{file_name}'".encode('utf-8'))
                receive_file(client, file_name)
                broadcast_file(file_name)

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
def broadcast_file(file_name):
    try:
        with open(file_name, 'rb') as file:
            file_data = file.read(5 * 1024 * 1024)
        message = f"File {file_name}".encode('utf-8')
        for client in clients:
            client.send(message)
            client.send(file_data)
        print(f"File '{file_name}' broadcasted to all clients")
    except Exception as e:
        print("An error occurred:", e)

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

def receive_file(client, file_name):
    try:
        file_data = client.recv(5 * 1024 * 1024)
        with open(file_name, 'wb') as file:
            file.write(file_data)
        print(f"File '{file_name}' received")
    except Exception as e:
        print("An error occurred:", e)

receive_connections()
