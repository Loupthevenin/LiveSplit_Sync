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
