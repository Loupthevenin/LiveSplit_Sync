from connect import Connect
from constants.order import *
from analyser import convert_time_format

unique_delta_values = []
unique_final_values = []
unique_split_index_values = []
unique_timer_phase_value = [""]


def get_delta_time(client):
    global unique_delta_values

    client.send_data(getdelta)
    data = client.receive_data()

    if data == '-':
        return False

    if not unique_delta_values or data != unique_delta_values[-1]:
        unique_delta_values.append(data)
        return data


def get_final_time(client):
    global unique_final_values

    client.send_data(getfinaltime_comp)
    data = client.receive_data()

    if data == "0.00.00":
        return False

    if not unique_final_values or data != unique_final_values[-1]:
        unique_final_values.append(data)
        return data


def get_timer_phase(client):
    global unique_timer_phase_value

    client.send_data(gettimerphase)
    data = client.receive_data()

    if data == "NotRunning" and unique_timer_phase_value[-1] == "Running":
        unique_timer_phase_value.append(data)
        return True
    else:
        unique_timer_phase_value.append(data)
        return False


def main():
    SERVER_IP = '127.168.1.27'
    PORT = 16834

    client = Connect(SERVER_IP, PORT)
    client.connect()

    while True:
        # DELTA TIME
        delta_time = get_delta_time(client)

        if delta_time:
            time_format = convert_time_format(delta_time)
            print(time_format)
            # faire tout le reste le temps a été split

        # FINAL TIME
        final_time = get_final_time(client)

        if final_time:
            time_format = convert_time_format(final_time)
            print(time_format)

        # RESET
        is_reset = get_timer_phase(client)

        if is_reset:
            print("-")


if __name__ == '__main__':
    main()
