from connect import Connect
from constants.order import *


def main():
    SERVER_IP = '127.168.1.27'
    PORT = 16834

    client = Connect(SERVER_IP, PORT)
    client.connect()

    while True:
        client.send_data(getcurrentrealtime)
        data = client.receive_data()
        print(data, type(data))


if __name__ == '__main__':
    main()
