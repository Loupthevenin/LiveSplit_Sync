from connect import workbook


# sheets = map(lambda x: x.title, workbook.worksheets())


def how_many_split() -> int:
    sheet = workbook.get_worksheet(1)
    splits = sheet.row_values(1)

    # Colonne supplémentaire necessaire pour le tableau ici 4 par defaut => coherence sur le sheets
    splits = len(splits) - 4

    return splits


def current_split():
    pass


split = how_many_split()

print(split)
