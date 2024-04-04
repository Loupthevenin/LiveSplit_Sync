
# VERSION // 1 = OUI // 2 = NON

#####################
#####################
#####################
VERSION_EXCEL = 0
VERSION_SHEETS = 1

VERSION_DELTA = 1
VERSION_TIME = 1
#####################
#####################
#####################


# Row par defaut
#####################
nb_row_edit = 3
nb_row_head = 1
#####################

# Cols par defaut
#####################
nb_cols_before_split_sheets = 3
nb_cols_total_head = 5
#####################


# Worksheet par defaut
#####################
index_worksheets = 1
#####################


# Cols head
#####################
col_ID = 1
col_date = 2
col_type = 3
#####################


# Precedent Row
#####################
row_pre_ID = nb_row_edit + 2 if (VERSION_DELTA + VERSION_TIME) > 1 else nb_row_edit + 1
#####################


# LiveSplit Server
#####################
SERVER_IP = '127.168.1.27'
PORT = 16834
#####################


# PATH EXCEL
#####################
xls = r"C:\Users\agent.mpr2\Documents\Code\LiveSplit_Sync\excel\run.xlsx"
path_excel = r"G:\Loup\Python\Projet\LiveSplit_Sync\excel\run.xlsx"
#####################
