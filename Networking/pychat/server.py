import threading
import socket

host = 'localhost' # localhost
port = 55000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()


clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)
    
def handle(client):
    while True:
        try:
            print("waiting for message")
            message = client.recv(1024)
            if message.decode('ascii') == "":
                break
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break
    

def receive():
    while True:
        print("waiting for connection")
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} has joined the chat'.encode('ascii'))
        client.send('Connected to server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("server is listening")
receive()