import datetime

from configs.configs import *
from connect import Connect
from analyser import convert_time_format, get_delta_time, get_final_time, get_timer_phase, get_split_index, get_last_time


VERSION = ""


if VERSION_SHEETS:
    if (VERSION_DELTA + VERSION_TIME) > 1:
        from tools.sheets_tools.sync_delta_time import *
        VERSION = "D+T+S"
    elif VERSION_DELTA:
        from tools.sheets_tools.sync_delta import *
        VERSION = "D+S"
    else:
        # autre sync_time ?
        pass
else:
    if (VERSION_DELTA + VERSION_TIME) > 1:
        from tools.excel_tools.sync_delta_time import *
        VERSION = "D+T+E"
    elif VERSION_DELTA:
        from tools.excel_tools.sync_delta import *
        VERSION = "D+E"
    else:
        # autre sync_time ?
        pass


def if_final_time(time_list, save_time_format):
    # split_index = current_split()
    split_index = len(time_list) + nb_cols_before_split_sheets + 1
    if is_pb(split_index, save_time_format):
        write_time(delta_time=save_time_format, index_col=split_index)
        if VERSION in ["D+T+E", "D+T+S"]:
            write_time(time=save_time_format, index_col=split_index)
    else:
        write_time(delta_time=save_time_format, index_col=(split_index + 1))
        if VERSION in ["D+T+E", "D+T+S"]:
            write_time(time=save_time_format, index_col=(split_index + 1))
    time_list.append(save_time_format)
    new_row()
    time_list.clear()


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
            date = str(datetime.datetime.now())[:-7]
            write_start(date)

        # DELTA TIME
        delta_time = get_delta_time(client)

        if delta_time:
            time_format = convert_time_format(delta_time)
            print(time_format)

            split_index = int(get_split_index(client)) + nb_cols_before_split_sheets
            if split_index == len(time_list) + nb_cols_before_split_sheets + 1:
                if write_time(delta_time=time_format, index_col=split_index):
                    time_list.append(time_format)
                else:
                    write_time(delta_time="-", index_col=split_index)
                    time_list.append(time_format)
            else:
                print("Decalage avec le sheets")

        # SI je mets le last time dans le delta time => un decalage de 1 dans le classeur
        # LAST TIME
        if VERSION in ["D+T+E", "D+T+S"]:
            index_split = int(get_split_index(client))
            if index_split > 0:
                last_time = get_last_time(client)
                if last_time:
                    last_time = convert_time_format(last_time)
                    write_time(time=last_time, index_col=(current_split(is_time=True)))

        # FINAL TIME
        final_time = get_final_time(client)
        if final_time:
            time_format = convert_time_format(final_time)
            save_time_format = time_format
            print(time_format)

            if len(time_list) == total_splits:
                if_final_time(time_list, save_time_format)
            elif len(time_list) < total_splits:
                waiting = True
                continue
        elif waiting:
            if len(time_list) == total_splits:
                if_final_time(time_list, save_time_format)
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
