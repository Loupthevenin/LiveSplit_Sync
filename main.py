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
        if get_timer_phase(client, start=True):
            date = str(datetime.datetime.now())
            write_start(date)

        # DELTA TIME
        delta_time = get_delta_time(client)

        if delta_time:
            time_format = convert_time_format(delta_time)
            print(time_format)

            split_index = int(get_split_index(client)) + nb_cols_before_split_sheets
            # if split_index == current_split():
            if split_index == len(time_list) + nb_cols_before_split_sheets + 1:
                if write_time(time_format, split_index):
                    time_list.append(time_format)
                else:
                    write_time("-", split_index)
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

            if len(time_list) == total_splits:
                # split_index = current_split()
                split_index = len(time_list) + nb_cols_before_split_sheets + 1
                write_time(save_time_format, split_index)
                time_list.append(save_time_format)
                new_row()
                time_list.clear()
            elif len(time_list) < total_splits:
                waiting = True
                continue
        elif waiting:
            if len(time_list) == total_splits:
                # split_index = current_split()
                split_index = len(time_list) + nb_cols_before_split_sheets + 1
                write_time(save_time_format, split_index)
                time_list.append(save_time_format)
                new_row()
                time_list.clear()
                waiting = False

        # RESET
        if get_timer_phase(client, reset=True):
            if get_split_index(client) == '-1':
                split_index = len(time_list) + nb_cols_before_split_sheets + 1
                write_reset(split_index)
                new_row()
                time_list.clear()


if __name__ == '__main__':
    main()
