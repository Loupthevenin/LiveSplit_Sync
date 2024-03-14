from connect import workbook
from constants.configs import *


# sheets = map(lambda x: x.title, workbook.worksheets())


def how_many_split() -> int:
    sheet = workbook.get_worksheet(index_worksheets)
    splits = sheet.row_values(nb_row_head)

    # Colonne supplémentaire necessaire pour le tableau ici 4 par defaut => coherence sur le sheets
    splits = len(splits) - nb_cols_total_head

    return splits


def current_split() -> int:
    sheet = workbook.get_worksheet(index_worksheets)
    values = sheet.row_values(nb_row_edit)

    return len(values) + 1


def new_row():
    sheet = workbook.get_worksheet(index_worksheets)
    sheet.insert_row(index=nb_row_edit)


def write_time(time, index_col) -> bool:
    sheet = workbook.get_worksheet(index_worksheets)
    is_none = sheet.cell(nb_row_edit, index_col).value == None

    print(is_none)

    if is_none:
        sheet.update_cell(nb_row_edit, index_col, time)
        return True
    else:
        return False


def write_start(date) -> bool:
    sheet = workbook.get_worksheet(index_worksheets)
    is_none_A = True if sheet.cell(nb_row_edit, col_ID).value == '' else False
    is_none_B = True if sheet.cell(nb_row_edit, col_date).value == '' else False

    if is_none_A and is_none_B:
        ID = sheet.cell(row_pre_ID, col_ID).value
        if ID == "":
            ID = 1
        else:
            ID += 1
        sheet.update_cells([(nb_row_edit, col_ID, ID), (nb_row_edit, col_date, date)])
        return True
    else:
        return False


def write_reset():
    sheet = workbook.get_worksheet(index_worksheets)
    values_splits = sheet.row_values(nb_row_edit)

    reset_col = len(values_splits) + 1

    sheet.cell(nb_row_edit, reset_col, "RESET")
