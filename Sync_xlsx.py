import xlwings as xw
from constants.configs import *
from analyser import find_pb


# CONNECT EXCEL
path_file = r"C:\Users\agent.mpr2\Documents\Code\LiveSplit_Sync\excel\run.xlsx"
sheet = xw.Book(path_file).sheets[index_worksheets]


def how_many_split() -> int:
    splits = sheet.range(nb_row_head, 1).end('right').column

    # Colonne supplémentaire necessaire pour le tableau ici 4 par defaut => coherence sur le sheets
    splits = splits - nb_cols_total_head

    return splits


def current_split() -> int:
    values = sheet.range((nb_row_edit, 1)).end('right').column
    print(values)
    return values + 1


# Ajouter l'ID dans new row car opti de l'API
def new_row():
    sheet.api.Rows(nb_row_edit).Insert()


def write_time(time, index_col) -> bool:
    try:
        sheet.range((nb_row_edit, index_col)).value = time
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


def is_pb(index_col):
    pb_values = sheet.col_values(index_col)
    print(pb_values)
    pb_values.pop(0)
    if find_pb(pb_values) != 0:
        pass
