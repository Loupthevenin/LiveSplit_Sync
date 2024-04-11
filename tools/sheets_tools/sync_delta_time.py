from connect import connect_sheet
from app.configs.settings import *
from analyser import convert_to_seconds


workbook = connect_sheet()
sheet = workbook.get_worksheet(index_worksheets)


def how_many_split() -> int:
    splits = sheet.row_values(nb_row_head)

    # Colonne supplémentaire necessaire pour le tableau ici 4 par defaut => coherence sur le sheets
    splits = len(splits) - nb_cols_total_head
    if splits < 0:
        print("WARNING ADD COLS", splits)

    return splits


def current_split(is_time=False) -> int:
    if is_time:
        values = sheet.row_values(nb_row_edit + 1)
    else:
        values = sheet.row_values(nb_row_edit)
    return len(values) + 1


# Ajouter l'ID dans new row car opti de l'API
def new_row():
    sheet.insert_row([], index=nb_row_edit)
    sheet.insert_row([], index=nb_row_edit)


# Modifier le write time pour considerer les 2 lignes à modifier et new_row + 1 penser a une colonne en plus etc
def write_time(index_col, delta_time=False,  time=False) -> bool:
    try:
        if delta_time:
            sheet.update_cell(nb_row_edit, index_col, delta_time)
        if time:
            sheet.update_cell((nb_row_edit + 1), index_col, time)
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

        value_type_delta = "DELTA"
        value_type_time = "TIME"

        sheet.update_cell(nb_row_edit, col_ID, int(ID))
        sheet.update_cell((nb_row_edit + 1), col_ID, int(ID))
        sheet.update_cell(nb_row_edit, col_date, date)
        sheet.update_cell((nb_row_edit + 1), col_date, date)
        sheet.update_cell(nb_row_edit, col_type, value_type_delta)
        sheet.update_cell((nb_row_edit + 1), col_type, value_type_time)
    except:
        print("Erreur START")


def write_reset(reset_col):
    sheet.update_cell(nb_row_edit, reset_col, "RESET")
    sheet.update_cell((nb_row_edit + 1), reset_col, "RESET")


def is_pb(index_col_pb, time_to_compare) -> bool:
    pb_values = sheet.col_values(index_col_pb)

    if len(pb_values) <= 1:
        return True
    last_pb = pb_values[1]
    if int(convert_to_seconds(last_pb)) > int(convert_to_seconds(time_to_compare)):
        return True
    else:
        return False
