import socket   
import threading
import time

username = input("Enter your username: ")

host = '127.0.0.1'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive_user_list():#recibir lista de clientes conectados
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith("ChatBot: Usuarios conectados:"):
                print(message)
            else:
                print(message)
        except:
            break

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("An error Ocurred")
            client.close
            break

def write_messages():
    while True:
        message = input('')
        client.send(f"{username}: {message}".encode("utf-8"))

def disconnect():
    client.send("QUIT".encode("utf-8"))
    client.close()

user_list_thread = threading.Thread(target=receive_user_list)
user_list_thread.start()

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()