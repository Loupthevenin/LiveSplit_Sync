import datetime
import threading

from PySide6 import QtWidgets
from PySide6.QtGui import QIcon


from app.configs.settings import (VERSION_SHEETS, VERSION_EXCEL, VERSION_TIME, VERSION_DELTA, SERVER_IP, PORT, nb_cols_before_split_sheets)
from connect import Connect
from analyser import convert_time_format, convert_seconds_to_time_format, convert_to_seconds, get_delta_time, get_final_time, get_timer_phase, get_split_index, get_last_time
from app.app import App


# def version_import():
#     VERSION = ""
#
#     if VERSION_SHEETS:
#         if (VERSION_DELTA + VERSION_TIME) > 1:
#             from tools.sheets_tools.sync_delta_time import how_many_split, current_split, new_row, write_time, write_start, write_reset, is_pb
#             VERSION = "D+T+S"
#         elif VERSION_DELTA:
#             from tools.sheets_tools.sync_delta import how_many_split, current_split, new_row, write_time, write_start, write_reset, is_pb
#             VERSION = "D+S"
#         else:
#             # autre sync_time ?
#             pass
#     else:
#         if (VERSION_DELTA + VERSION_TIME) > 1:
#             from tools.excel_tools.sync_delta_time import how_many_split, current_split, new_row, write_time, write_start, write_reset, is_pb
#             VERSION = "D+T+E"
#         elif VERSION_DELTA:
#             from tools.excel_tools.sync_delta import how_many_split, current_split, new_row, write_time, write_start, write_reset, is_pb
#             VERSION = "D+E"
#         else:
#             # autre sync_time ?
#             pass

# TODO J'utilise un thread pour le background problème : TOUT doit etre chargé dans le meme Thread donc import etc... (+ par rapport a xlwings)
# TODO Et reflechir a un code plus synthetique sur main

def if_final_time(delta_list, time_list, save_time_format, is_pb):
    split_index = len(delta_list) + nb_cols_before_split_sheets + 1
    if is_pb(split_index, save_time_format):
        write_time(delta_time=save_time_format, index_col=split_index)
        if VERSION in ["D+T+E", "D+T+S"]:
            write_time(time=save_time_format, index_col=split_index)
    else:
        write_time(delta_time=save_time_format, index_col=(split_index + 1))
        if VERSION in ["D+T+E", "D+T+S"]:
            write_time(time=save_time_format, index_col=(split_index + 1))
    delta_list.append(save_time_format)
    time_list.append(save_time_format)
    new_row()
    delta_list.clear()
    time_list.clear()


def main():
    # version_import()
    VERSION = ""

    if VERSION_SHEETS:
        if (VERSION_DELTA + VERSION_TIME) > 1:
            from tools.sheets_tools.sync_delta_time import how_many_split, current_split, new_row, write_time, \
                write_start, write_reset, is_pb
            VERSION = "D+T+S"
        elif VERSION_DELTA:
            from tools.sheets_tools.sync_delta import how_many_split, current_split, new_row, write_time, write_start, \
                write_reset, is_pb
            VERSION = "D+S"
        else:
            # autre sync_time ?
            pass
    else:
        if (VERSION_DELTA + VERSION_TIME) > 1:
            from tools.excel_tools.sync_delta_time import how_many_split, current_split, new_row, write_time, \
                write_start, write_reset, is_pb
            VERSION = "D+T+E"
        elif VERSION_DELTA:
            from tools.excel_tools.sync_delta import how_many_split, current_split, new_row, write_time, write_start, \
                write_reset, is_pb
            VERSION = "D+E"
        else:
            # autre sync_time ?
            pass

    client = Connect(SERVER_IP, PORT)
    client.connect()

    waiting = False
    save_time_format = ""

    delta_time_list = []
    time_split_list = []
    total_splits = how_many_split()

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
            if split_index == len(delta_time_list) + nb_cols_before_split_sheets + 1:
                if write_time(delta_time=time_format, index_col=split_index):
                    delta_time_list.append(time_format)
                else:
                    write_time(delta_time="-", index_col=split_index)
                    delta_time_list.append(time_format)
            else:
                print("Decalage avec le sheets")

        # LAST TIME
        if VERSION in ["D+T+E", "D+T+S"]:
            index_split = int(get_split_index(client))
            if index_split > 0:
                last_time = get_last_time(client)
                if last_time:
                    last_time = convert_time_format(last_time)
                    if time_split_list:
                        last_time_seconds = convert_to_seconds(last_time)
                        last_previous_time_seconds = convert_to_seconds(time_split_list[-1])
                        last_time = convert_seconds_to_time_format(round((last_time_seconds - last_previous_time_seconds), 2))
                    write_time(time=last_time, index_col=(current_split(is_time=True)))
                    time_split_list.append(last_time)
                elif len(delta_time_list) > len(time_split_list):
                    write_time(time="-", index_col=(current_split(is_time=True)))
                    time_split_list.append("-")

        # FINAL TIME
        final_time = get_final_time(client)
        if final_time:
            time_format = convert_time_format(final_time)
            save_time_format = time_format
            print(time_format)

            if len(delta_time_list) == total_splits:
                if_final_time(delta_time_list, time_split_list, save_time_format, is_pb)
            elif len(delta_time_list) < total_splits:
                waiting = True
                continue
        elif waiting:
            if len(delta_time_list) == total_splits:
                if_final_time(delta_time_list, time_split_list, save_time_format, is_pb)
                waiting = False

        # RESET
        if get_timer_phase(client, reset=True):
            if get_split_index(client) == '-1':
                split_index = len(delta_time_list) + nb_cols_before_split_sheets + 1
                write_reset(split_index)
                new_row()
                delta_time_list.clear()
                time_split_list.clear()


def run_thread_main():
    thread_main_loop = threading.Thread(target=main)
    thread_main_loop.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QIcon('app/images/LiveSplit_ico.ico'))
    win = App()
    win.resize(800, 600)
    win.show()
    win.main_loop_signal.connect(run_thread_main)
    app.exec()
