from configs.order import *


unique_delta_values = []
unique_time_values = []
unique_final_values = []
unique_timer_phase_value_reset = [""]
unique_timer_phase_value_start = [""]


def delete_value(values_list):
    nb_size = 20
    values_list = values_list[-nb_size:]
    return values_list


def convert_time_format(time_str):

    if "-" in time_str:
        time_str = time_str.replace("-", "")
        time_diff = "-"
    elif "+" in time_str:
        time_str = time_str.replace("+", "")
        time_diff = "+"
    elif ":" in time_str:
        time_str = time_str.replace(":", ".")
        time_diff = ""
    else:
        time_diff = ""

    parts = time_str.split('.')

    if len(parts) == 1:
        miliseconds = parts[0].zfill(2)
        seconds = '00'
        minutes = '00'
        hours = '0'
    elif len(parts) == 2:
        miliseconds = parts[-1].zfill(2)
        seconds = parts[-2].zfill(2)
        minutes = '00'
        hours = '0'
    elif len(parts) == 3:
        miliseconds = parts[-1].zfill(2)
        seconds = parts[-2].zfill(2)
        minutes = parts[-3].zfill(2)
        hours = '0'
    elif len(parts) == 4:
        miliseconds = parts[-1].zfill(2)
        seconds = parts[-2].zfill(2)
        minutes = parts[-3].zfill(2)
        hours = parts[-4].zfill(2)
    else:
        miliseconds = '00'
        seconds = '00'
        minutes = '00'
        hours = '0'

    return f"'{time_diff}{hours}:{minutes}:{seconds},{miliseconds}"


def convert_to_seconds(time_str):
    parts = time_str.replace("'", "").split(":")
    print(parts)
    seconds_parts = parts[-1].split(',')

    # PROBlEME AVEC LES MILISECONDES

    seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(seconds_parts[0]) + int(seconds_parts[1]) / 100

    return seconds


def get_delta_time(client):
    global unique_delta_values

    client.send_data(getdelta)
    data = client.receive_data()

    if data == '-':
        return False

    if not unique_delta_values or data != unique_delta_values[-1]:
        unique_delta_values.append(data)
        unique_delta_values = delete_value(unique_delta_values)
        return data


# Decider si on garde le temps global ou si on garde le temps AU split
# Faire en sorte de trouver une echappatoire pour ne pas arreter le script
def get_last_time(client):
    global unique_time_values

    # Entre ici
    client.send_data(getlastsplittime)
    data = client.receive_data()
    # Et ici

    if not unique_time_values or data != unique_time_values[-1]:
        unique_time_values.append(data)
        unique_time_values = delete_value(unique_time_values)
        return data
    else:
        return False


def get_final_time(client):
    global unique_final_values

    client.send_data(getfinaltime_comp)
    data = client.receive_data()

    if data == "0.00.00":
        return False

    if not unique_final_values or data != unique_final_values[-1]:
        unique_final_values.append(data)
        unique_final_values = delete_value(unique_final_values)
        return data


def get_timer_phase(client, reset=False, start=False):
    global unique_timer_phase_value_reset, unique_timer_phase_value_start

    client.send_data(gettimerphase)
    data = client.receive_data()

    if data == "NotRunning" and unique_timer_phase_value_reset[-1] == "Running" and reset:
        unique_timer_phase_value_reset.append(data)
        unique_timer_phase_value_reset = delete_value(unique_timer_phase_value_reset)
        return True
    elif data == "Running" and unique_timer_phase_value_start[-1] == "NotRunning" and start:
        unique_timer_phase_value_start.append(data)
        unique_timer_phase_value_start = delete_value(unique_timer_phase_value_start)
        return True
    elif reset:
        unique_timer_phase_value_reset.append(data)
        unique_timer_phase_value_reset = delete_value(unique_timer_phase_value_reset)
        return False
    elif start:
        unique_timer_phase_value_start.append(data)
        unique_timer_phase_value_start = delete_value(unique_timer_phase_value_start)
        return False


def get_split_index(client):
    client.send_data(getsplitindex)
    data = client.receive_data()

    if data:
        return data
    else:
        return False
