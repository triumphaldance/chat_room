import socket
from threading import Thread, Lock


class ChatClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.sockU = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.coordinator_address = (server_host, server_port)
        self.sockT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, message):
        self.sockU.sendto(message.encode(), self.coordinator_address)
        response, _ = self.sockU.recvfrom(1024)
        print("Received:", response.decode())
        message = response.decode()
        if message.startswith('JOIN'):
            server_addr = int(message.split()[-1].replace(')', ''))
            # 连接到服务器
            self.sockT.connect(('localhost', server_addr))
        elif message.endswith('FOUND'):
            print("Please try again")
        else:

            server_addr = int(message.split()[5])
            # 连接到服务器
            self.sockT.connect(('localhost', server_addr))

    def start_chat_session(self):
        self.send_message("CREATE")

    def join_chat_session(self, session_id):
        self.send_message(f"JOIN {session_id}")

    def chat(self, message):
        self.sockT.sendall(message.encode())

    def receive_message(self):
        thread_stop = True
        while thread_stop:
            response = self.sockT.recv(1024).decode()
            print('-----------------------------------------------------')
            print("Received:", response)
            # print("Received:", response)
        # print("No message received.")
        # try:
        #     response = self.sockT.recv(1024).decode()
        #     print("Received:", response)
        # except BlockingIOError:
        #     print("No message available.")

    def close_connection(self):
        self.sockT.close()


# 使用客户端
if __name__ == "__main__":
    client = ChatClient('localhost', 10000)
    cmd = input("Enter command (start/join/send/exit): ")
    while True:

        if cmd == 'start':
            client.start_chat_session()
            thread = Thread(target=client.receive_message)
            thread.start()  # 确保线程启动
        elif cmd.startswith('join'):
            _, session_id = cmd.split()
            client.join_chat_session(session_id)
            thread = Thread(target=client.receive_message)
            thread.start()  # 确保线程启动
        elif cmd.startswith('send'):
            _, message = cmd.split(maxsplit=1)
            client.chat(message)

        elif cmd == 'exit':
            thread_stop = False
            client.chat('EXIT')
            client.close_connection()
            break
        cmd = input()




#### test