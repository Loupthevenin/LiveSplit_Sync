import datetime

from connect import Connect
from constants.order import *
from analyser import convert_time_format
from Sync import *
from constants.configs import *


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


def get_timer_phase(client, reset=False, start=False):
    global unique_timer_phase_value

    client.send_data(gettimerphase)
    data = client.receive_data()

    if data == "NotRunning" and unique_timer_phase_value[-1] == "Running" and reset:
        unique_timer_phase_value.append(data)
        return True
    elif data == "Running" and unique_timer_phase_value[-1] == "NotRunning" and start:
        unique_timer_phase_value.append(data)
        return True
    else:
        unique_timer_phase_value.append(data)
        return False


def get_split_index(client):
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

    waiting = False
    save_time_format = ""

    # Au moment ou on lance le server ID date pas remplis

    while True:
        # Start run
        is_start = get_timer_phase(client, start=True)

        if is_start:
            date = datetime.datetime.now()
            write_start(date)

        # DELTA TIME
        delta_time = get_delta_time(client)

        if delta_time:
            time_format = convert_time_format(delta_time)
            print(time_format)

            split_index = get_split_index(client)
            if split_index:
                print(f"Split index delta time : {split_index}")
                # +1 car commence a 0 et 2 cols donc +3
                split_index = int(split_index) + nb_cols_before_split_sheets

                if split_index == current_split():
                    write_time(time_format, split_index)
                else:
                    print("Decalage avec le sheets")

        # FINAL TIME
        final_time = get_final_time(client)
        # Problème il renvois vrai quand on lance le server
        if final_time:
            time_format = convert_time_format(final_time)
            save_time_format = time_format
            print(time_format)
            total_split = (current_split() - nb_cols_before_split_sheets - 1)

            if total_split == how_many_split():
                split_index = current_split()
                write_time(save_time_format, split_index)
            elif total_split < how_many_split():
                waiting = True
                continue
        elif waiting:
            total_split = (current_split() - nb_cols_before_split_sheets - 1)
            if total_split == how_many_split():
                split_index = current_split()
                write_time(save_time_format, split_index)
                waiting = False

        # RESET
        is_reset = get_timer_phase(client, reset=True)

        if is_reset:
            print("-")
            split_index = get_split_index(client)
            if split_index:
                print(f"Split index reset : {split_index}")
                if split_index == '-1':
                    write_reset()
                    new_row()


if __name__ == '__main__':
    main()
