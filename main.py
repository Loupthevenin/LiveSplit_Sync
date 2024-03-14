from connect import Connect
from constants.order import *
from analyser import convert_time_format
from Sync import *


unique_delta_values = []
unique_final_values = []
# unique_split_index_values = []
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


def get_slipt_index(client):
    client.send_data(getsplitindex)
    data = client.receive_data()

    if data:
        return data
    else:
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

            split_index = get_slipt_index(client)
            if split_index:
                print(f"Split index delta time : {split_index}")
                # +1 car commence a 0 et 2 cols donc +3
                split_index = int(split_index) + 3

                if split_index == current_split():
                    write_time(time_format, split_index)
                else:
                    print("Decalage avec le sheets")

        # FINAL TIME
        final_time = get_final_time(client)

        if final_time:
            time_format = convert_time_format(final_time)
            print(time_format)
            split_index = get_slipt_index(client)
            if split_index:
                print(f"Split index final time : {split_index}")
                if split_index == '-1':
                    split_index = how_many_split() + 3
                    write_time(time_format, split_index)

        # RESET
        is_reset = get_timer_phase(client)

        if is_reset:
            print("-")
            split_index = get_slipt_index(client)
            if split_index:
                print(f"Split index reset : {split_index}")
                if split_index == '-1':
                    write_reset()
                    new_row()


if __name__ == '__main__':
    main()
