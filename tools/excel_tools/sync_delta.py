import xlwings as xw
from app.configs.settings import (path_excel, index_worksheets, nb_row_head, nb_cols_total_head, nb_row_edit, col_ID, col_date, row_pre_ID)
from analyser import convert_to_seconds


# CONNECT EXCEL
sheet = xw.Book(path_excel).sheets[index_worksheets]


def how_many_split() -> int:
    splits = sheet.range(nb_row_head, 1).end('right').column

    # Colonne supplémentaire necessaire pour le tableau ici 4 par defaut => coherence sur le sheets
    splits = splits - nb_cols_total_head
    if splits < 0:
        print("WARNING ADD COLS", splits)

    return splits


def current_split(is_time=False) -> int:
    if is_time:
        values = sheet.range(((nb_row_edit + 1), 1)).end('right').column
    else:
        values = sheet.range((nb_row_edit, 1)).end('right').column
    return values + 1


def new_row():
    sheet.api.Rows(nb_row_edit).Insert()


def write_time(delta_time, index_col) -> bool:
    try:
        sheet.range((nb_row_edit, index_col)).value = delta_time
        return True
    except:
        return False


def write_start(date):
    try:
        ID = sheet.range((row_pre_ID, col_ID)).value
        if ID is None:
            ID = 1
        else:
            ID = int(ID) + 1
        sheet.range((nb_row_edit, col_ID)).value = int(ID)
        sheet.range((nb_row_edit, col_date)).value = date
    except:
        print("Erreur START")


def write_reset(reset_col):
    sheet.range((nb_row_edit, reset_col)).value = "RESET"


def is_pb(index_col_pb, time_to_compare) -> bool:
    pb_values = sheet.range((nb_row_edit, index_col_pb), (sheet.cells.last_cell.row, index_col_pb)).value
    pb_values = [value for value in pb_values if value is not None]

    if not pb_values:
        return True
    last_pb = pb_values[0]
    if int(convert_to_seconds(last_pb)) > int(convert_to_seconds(time_to_compare)):
        return True
    else:
        return False
