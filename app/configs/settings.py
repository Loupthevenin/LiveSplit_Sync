import json


with open("settings.json", "r") as f:
    settings_json = json.load(f)


# VERSION // 1 = OUI // 2 = NON

#####################
#####################
#####################
VERSION_EXCEL = settings_json["VERSION"]["VERSION_EXCEL"]
VERSION_SHEETS = settings_json["VERSION"]["VERSION_SHEETS"]

VERSION_DELTA = settings_json["VERSION"]["VERSION_DELTA"]
VERSION_TIME = settings_json["VERSION"]["VERSION_TIME"]
#####################
#####################
#####################


# Row par defaut
#####################
nb_row_edit = settings_json["TABLE"]["nb_row_edit"]
nb_row_head = settings_json["TABLE"]["nb_row_head"]
#####################

# Cols par defaut
#####################
nb_cols_before_split_sheets = settings_json["TABLE"]["nb_cols_before_split_sheets"]
nb_cols_total_head = settings_json["TABLE"]["nb_cols_total_head"]
#####################


# Worksheet par defaut
#####################
index_worksheets = settings_json["TABLE"]["index_worksheets"]
#####################


# Cols head
#####################
col_ID = settings_json["TABLE"]["col_ID"]
col_date = settings_json["TABLE"]["col_date"]
col_type = settings_json["TABLE"]["col_type"]
#####################


# Precedent Row
#####################
row_pre_ID = nb_row_edit + 2 if (VERSION_DELTA + VERSION_TIME) > 1 else nb_row_edit + 1
#####################


# LiveSplit Server
#####################
SERVER_IP = settings_json["SERVER"]["SERVER_IP"]
PORT = settings_json["SERVER"]["PORT"]
#####################


# Path
#####################
path_excel = settings_json["PATH"]["path_excel"]
sheet_id = settings_json["PATH"]["sheet_id"]
#####################
