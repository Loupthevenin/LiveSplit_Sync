from connect import Connect
from constants.order import *
from datetime import time, datetime, timedelta

unique_delta_values = []
unique_final_values = []
unique_split_index_values = []
unique_timer_phase_values = []


def get_unique_delta_time(data):
    global unique_delta_values

    if data == '-':
        return False

    time_t = data.replace('.', ':')

    if not unique_delta_values or time_t != unique_delta_values[-1]:
        unique_delta_values.append(time_t)
        return time_t


def get_unique_final_time(data):
    global unique_final_values

    if data == "0.00.00":
        return False

    time_t = data.replace('.', ':')

    if not unique_final_values or time_t != unique_final_values[-1]:
        unique_final_values.append(time_t)
        return time_t


def main():
    SERVER_IP = '127.168.1.27'
    PORT = 16834

    client = Connect(SERVER_IP, PORT)
    client.connect()

    while True:
        client.send_data(getdelta)
        data = client.receive_data()
        print(data)
        unique_delta_time = get_unique_delta_time(data)

        if unique_delta_time:
            print(unique_delta_time, type(unique_delta_time))
            # faire tout le reste le temps a été split

        client.send_data(getfinaltime_comp)
        data = client.receive_data()
        unique_final_time = get_unique_final_time(data)

        if unique_final_time:
            print(unique_final_time, type(unique_final_time))


if __name__ == '__main__':
    main()
