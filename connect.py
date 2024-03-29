import socket
import gspread
from google.oauth2.service_account import Credentials


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
            data = data.decode("utf-8").replace("\r\n", "").replace("−", "-")
            return data

    def send_data(self, message):
        self.sock.send(message.encode('utf-8'))

    def close(self):
        self.sock.close()


# CONNECT GOOGLE SHEETS
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "14v8vv4tpFQh4PYhelx6EI2fDA5FPhbWTVX7d6gIyOf0"
workbook = client.open_by_key(sheet_id)
