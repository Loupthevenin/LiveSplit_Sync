import datetime

from connect import Connect
from analyser import convert_time_format, get_delta_time, get_final_time, get_timer_phase, get_split_index
from Sync import *
from constants.configs import *


def main():
    waiting = False
    save_time_format = ""

    time_list = []
    total_splits = how_many_split()

    client = Connect(SERVER_IP, PORT)
    client.connect()

    while True:
        # Start run
        is_start = get_timer_phase(client, start=True)

        if is_start:
            date = str(datetime.datetime.now())
            write_start(date)

        # DELTA TIME
        delta_time = get_delta_time(client)

        if delta_time:
            time_format = convert_time_format(delta_time)
            print(time_format)

            split_index = get_split_index(client)
            if split_index:
                split_index = int(split_index) + nb_cols_before_split_sheets

                # if split_index == current_split():
                if split_index == len(time_list) + nb_cols_before_split_sheets + 1:
                    write_time(time_format, split_index)
                    time_list.append(time_format)
                else:
                    print("Decalage avec le sheets")

        # FINAL TIME
        final_time = get_final_time(client)
        if final_time:
            time_format = convert_time_format(final_time)
            save_time_format = time_format
            print(time_format)
            # total_split = (current_split() - nb_cols_before_split_sheets - 1)
            total_split = len(time_list)

            if total_split == total_splits:
                # split_index = current_split()
                split_index = len(time_list) + nb_cols_before_split_sheets + 1
                write_time(save_time_format, split_index)
                time_list.append(time_format)
                new_row()
                time_list.clear()
            elif total_split < total_splits:
                waiting = True
                continue
        elif waiting:
            total_split = len(time_list)
            if total_split == total_splits:
                # split_index = current_split()
                split_index = len(time_list) + nb_cols_before_split_sheets + 1
                write_time(save_time_format, split_index)
                new_row()
                waiting = False

        # RESET
        is_reset = get_timer_phase(client, reset=True)
        if is_reset:
            split_index = get_split_index(client)
            if split_index:
                if split_index == '-1':
                    write_reset()
                    new_row()
                    time_list.clear()


if __name__ == '__main__':
    main()
