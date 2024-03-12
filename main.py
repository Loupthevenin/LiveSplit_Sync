from connect import Connect
from constants.order import *
from analyser import convert_time_format

unique_delta_values = []
unique_final_values = []
unique_split_index_values = []
unique_timer_phase_values = []


def get_unique_delta_time(data):
    global unique_delta_values

    if data == '-':
        return False

    if not unique_delta_values or data != unique_delta_values[-1]:
        unique_delta_values.append(data)
        return data


def get_unique_final_time(data):
    global unique_final_values

    if data == "0.00.00":
        return False

    if not unique_final_values or data != unique_final_values[-1]:
        unique_final_values.append(data)
        return data


def main():
    SERVER_IP = '127.168.1.27'
    PORT = 16834

    client = Connect(SERVER_IP, PORT)
    client.connect()

    while True:
        client.send_data(getdelta)
        data = client.receive_data()
        unique_delta_time = get_unique_delta_time(data)

        if unique_delta_time:
            time_format = convert_time_format(unique_delta_time)
            print(time_format)
            # faire tout le reste le temps a été split

        client.send_data(getfinaltime_comp)
        data = client.receive_data()
        unique_final_time = get_unique_final_time(data)

        if unique_final_time:
            time_formats = convert_time_format(unique_final_time)
            print(time_formats)


if __name__ == '__main__':
    main()
