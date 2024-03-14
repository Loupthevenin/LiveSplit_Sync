from connect import workbook
from constants.configs import *


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
    is_none = sheet.cell(nb_row_edit, index_col).value is None

    print(is_none)

    if is_none:
        sheet.update_cell(nb_row_edit, index_col, time)
        return True
    else:
        return False


def write_start(date):
    is_none_A = True if sheet.cell(nb_row_edit, col_ID).value is None else False
    is_none_B = True if sheet.cell(nb_row_edit, col_date).value is None else False

    if is_none_A and is_none_B:
        ID = sheet.cell(row_pre_ID, col_ID).value
        if ID is None:
            ID = 1
        else:
            ID = int(ID) + 1
        sheet.update_cell(nb_row_edit, col_ID, int(ID))
        sheet.update_cell(nb_row_edit, col_date, date)
    else:
        print("Erreur START")


def write_reset():
    values_splits = sheet.row_values(nb_row_edit)
    reset_col = len(values_splits) + 1
    sheet.update_cell(nb_row_edit, reset_col, "RESET")
