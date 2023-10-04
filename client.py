import socket
import threading

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "@username":
                client.send(username.encode("utf-8"))
            elif message.startswith("File"):
                print(message)
                file_name = message.split(' ')[1]
                file_data = client.recv(5 * 1024 * 1024)
                save_files(file_name, file_data)
                with open(file_name, 'wb') as file:
                    file.write(file_data)
                print(f"File '{file_name}' received and saved successfully")
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
        else:
            client.send(message.encode('utf-8'))

def send_files(file_name):
    try:
        with open(file_name, 'rb') as file:
            file_data = file.read(5 * 1024 * 1024)
            client.send(f"/send {file_name}".encode('utf-8'))
            chunk_size = 1024
            for i in range (0, len(file_data), chunk_size):
                chunk = file_data[i:i+chunk_size]
                client.send(chunk)
        print(f"File '{file_name}' sent successfully")
    except Exception as e:
        print("An error occurred")

def save_files(file_name, file_data):
    try:
        with open(file_name, 'wb') as file:
            file.write(file_data)
        print(f"File '{file_name}' received and saved successfully")
    except Exception as e:
        print("An error occurred:", e)

username = input("Enter your username: ")

host = '148.220.210.60'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()
