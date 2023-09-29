import socket   
import threading
import time

host = '127.0.0.1'
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


def send_users_list(): #enviar lista de clientes conectados cada 30 segundos
    while True:
        time.sleep(30)
        user_list = ", ".join(usernames)
        broadcast(f"ChatBot: Usuarios conectados: {user_list}".encode('utf-8'), None)

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
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

def handle_client_disconnect(client):
    index = clients.index(client)
    username = usernames[index]

    broadcast(f"ChatBot: {username} disconnected".encode('utf-8'), client)
    clients.remove(client)
    usernames.remove(username)

    print(f"{username} disconnected")


user_list_thread = threading.Thread(target=send_users_list)
user_list_thread.start()

receive_connections()

