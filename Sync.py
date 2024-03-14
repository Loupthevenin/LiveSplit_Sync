from connect import workbook


# sheets = map(lambda x: x.title, workbook.worksheets())
index_worksheets = 1


def how_many_split() -> int:
    sheet = workbook.get_worksheet(index_worksheets)
    splits = sheet.row_values(1)

    # Colonne supplémentaire necessaire pour le tableau ici 4 par defaut => coherence sur le sheets
    splits = len(splits) - 4

    return splits


def current_split() -> int:
    sheet = workbook.get_worksheet(index_worksheets)
    values = sheet.row_values(2)

    return len(values) + 1


def new_row():
    sheet = workbook.get_worksheet(index_worksheets)
    sheet.insert_row(index=2)


def write_time(time, index_col) -> bool:
    sheet = workbook.get_worksheet(index_worksheets)
    is_none = True if sheet.cell(2, index_col).value == '' else False

    if is_none:
        sheet.update_cell(2, index_col, time)
        return True
    else:
        return False


def write_start(date) -> bool:
    sheet = workbook.get_worksheet(index_worksheets)
    is_none_A = True if sheet.cell(2, 1).value == '' else False
    is_none_B = True if sheet.cell(2, 2).value == '' else False

    if is_none_A and is_none_B:
        ID = sheet.cell(3, 1).value
        sheet.update_cells([(2, 1, ID), (2, 2, date)])
        return True
    else:
        return False


split = how_many_split()

print(split)
