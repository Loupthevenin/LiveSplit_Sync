import socket


class Connect:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.server_ip, self.port))
        print('Connecté au serv')

    def receive_data(self):
        data = self.sock.recv(1024)
        if data:
            return data.decode("utf-8")

    def send_data(self, message):
        self.sock.send(message.encode('utf-8'))

    def close(self):
        self.sock.close()
