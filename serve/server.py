import socket
from threading import Thread

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

    def handle_client(self, client_socket, addr):
        while True:
            msg = client_socket.recv(1024).decode()
            print('(', self.port, ')', '[', addr, ']:', msg)
            if msg == 'EXIT':
                self.broadcast('A user quit group chat', client_socket)
                self.clients.remove(client_socket)
                break
            self.broadcast(msg, client_socket)

    def client_num(self, source):
        num = str(len(self.clients))
        message = 'There are ' + num + ' person in Group chats'
        source.sendall(message.encode())
    def broadcast(self, message, source):
        for client in self.clients:
            if client is not source:
                remote_addr = client.getpeername()
                print('Send To', remote_addr)
                source_addr = source.getpeername()
                complete_message = str(source_addr) + ': ' + message
                client.sendall(complete_message.encode())

    def run(self):
        print(f"Chat server running on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            self.client_num(client_socket)
            self.broadcast('A new user joins group chat', client_socket)
            print(f"Connection established with {addr}")
            thread = Thread(target=self.handle_client, args=(client_socket, addr))
            thread.start()

            if not self.clients:
                break

