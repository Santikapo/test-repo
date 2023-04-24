import socket
import threading

host = 'localhost'
port = 55000

nickname = input("Choose Nickname")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))

def recieve():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("an error occured")
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        if message == f'{nickname}: exit':
            client.close()
            break
        client.send(message.encode('ascii'))


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()