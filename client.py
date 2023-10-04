import socket
import threading
import struct
import os

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "@username":
                client.send(username.encode("utf-8"))
            elif message.startswith("File"):
                print("Receiving file...")
                

            else:
                print(message)
        except:
            print("An error occurred")
            client.close()
            break

def write_messages():
    while True:
        message = input('')
        if client.fileno() == -1:
            # Verifica si el socket del cliente está cerrado.
            print("Disconnected from server.")
            break
        if message.startswith('@'):
            recipient_username, private_message = message.split(' ', 1)
            client.send(f"{message}".encode('utf-8'))
        elif message.startswith('/send'):
            file_name = message.split(' ')[1]
            client.send(f"{message}".encode('utf-8'))
            send_files(file_name)
        else:
            client.send(message.encode('utf-8'))

def send_files(file_name):
    try:
        #informa al servidor la cantidad de bytes a enviar
        filesize = os.path.getsize(file_name)
        if filesize > 5 * 1024 * 1024:
            print("File too large")
            return
        else:
            client.sendall(struct.pack("<Q", filesize))
            with open(file_name, 'rb') as file:
                #envía el archivo en bloques de 1024 bytes
                while read_bytes := file.read(1024):
                    client.sendall(read_bytes)
                
    except Exception as e:
        print("An error occurred")


username = input("Enter your username: ")

host = '148.220.210.60'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()
