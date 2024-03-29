from connect import workbook
from constants.configs import *
from analyser import find_pb


# sheets = map(lambda x: x.title, workbook.worksheets())

sheet = workbook.get_worksheet(index_worksheets)


def how_many_split() -> int:
    splits = sheet.row_values(nb_row_head)

    # Colonne supplémentaire necessaire pour le tableau ici 4 par defaut => coherence sur le sheets
    splits = len(splits) - nb_cols_total_head

    return splits


def current_split() -> int:
    values = sheet.row_values(nb_row_edit)
    return len(values) + 1


# Ajouter l'ID dans new row car opti de l'API
def new_row():
    sheet.insert_row([], index=nb_row_edit)


def write_time(time, index_col) -> bool:
    try:
        sheet.update_cell(nb_row_edit, index_col, time)
        return True
    except:
        return False


def write_start(date):
    try:
        ID = sheet.cell(row_pre_ID, col_ID).value
        if ID is None:
            ID = 1
        else:
            ID = int(ID) + 1
        sheet.update_cell(nb_row_edit, col_ID, int(ID))
        sheet.update_cell(nb_row_edit, col_date, date)
    except:
        print("Erreur START")


def write_reset(reset_col):
    sheet.update_cell(nb_row_edit, reset_col, "RESET")


def is_pb(index_col):
    pb_values = sheet.col_values(index_col)
    print(pb_values)
    pb_values.pop(0)
    if find_pb(pb_values) != 0:
        pass
