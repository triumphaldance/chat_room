import socket
from server import ChatServer
from threading import Thread
class ChatCoordinator:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sessions = {}  # 存储会话信息，键为会话ID，值为对应的聊天服务器地址
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))

    def listen(self):
        print(f"Listening on {self.host}:{self.port}")
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = data.decode()
            print(f"Received message: {message} from {addr}")
            if message.startswith('CREATE'):
                self.create_session(addr)
            elif message.startswith('JOIN'):
                session_id = message.split()[1]
                self.join_session(session_id, addr)

    def create_session(self, addr):
        session_id = len(self.sessions) + 1
        # 假设每个新会话都在新的端口上启动一个聊天服务器
        session_port = self.port + session_id
        server = ChatServer('localhost', session_port)
        self.sessions[session_id] = ('localhost', session_port)
        print('sessions:', self.sessions)
        # 发送新会话信息给客户端
        self.sock.sendto(f"SESSION {session_id} CREATED AT PORT {session_port}".encode(), addr)
        thread = Thread(target=server.run)
        thread.start()  # 确保线程启动


    def join_session(self, session_id, addr):
        if int(session_id) in self.sessions:
            session_addr = self.sessions[int(session_id)]
            self.sock.sendto(f"JOIN {session_id} AT {session_addr}".encode(), addr)

        else:
            self.sock.sendto("SESSION NOT FOUND".encode(), addr)

# 运行协调器
if __name__ == "__main__":
    coordinator = ChatCoordinator('localhost', 10000)
    coordinator.listen()
