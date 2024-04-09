from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QDialog, QVBoxLayout, QGroupBox, QFormLayout, QCheckBox, QLineEdit, QPushButton
import json


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings_json = self.load_settings()

        self.settings_ui()

    def settings_ui(self):
        self.setWindowTitle("Settings")

        layout = QVBoxLayout()

        versions_settings_group = QGroupBox("Versions Settings")
        versions_settings_layout = QFormLayout()

        self.excel_version = QCheckBox(checked=(True if self.settings_json["VERSION"]["VERSION_EXCEL"] == "1" else False))
        self.sheets_version = QCheckBox(checked=(True if self.settings_json["VERSION"]["VERSION_SHEETS"] == "1" else False))
        self.delta_version = QCheckBox(checked=(True if self.settings_json["VERSION"]["VERSION_DELTA"] == "1" else False))
        self.time_version = QCheckBox(checked=(True if self.settings_json["VERSION"]["VERSION_TIME"] == "1" else False))

        versions_settings_layout.addRow("Excel version:", self.excel_version)
        versions_settings_layout.addRow("Sheets version:", self.sheets_version)
        versions_settings_layout.addRow("Delta:", self.delta_version)
        versions_settings_layout.addRow("Time", self.time_version)

        versions_settings_group.setLayout(versions_settings_layout)
        layout.addWidget(versions_settings_group)

        table_settings_group = QGroupBox("Table Settings")
        table_settings_layout = QFormLayout()

        self.index_worksheets = QLineEdit(None, validator=QIntValidator(), text=self.settings_json["TABLE"]["index_worksheets"])
        self.row_edit = QLineEdit(None, validator=QIntValidator(), text=self.settings_json["TABLE"]["nb_row_edit"])
        self.row_head = QLineEdit(None, validator=QIntValidator(), text=self.settings_json["TABLE"]["nb_row_head"])
        self.cols_before_split = QLineEdit(None, validator=QIntValidator(), text=self.settings_json["TABLE"]["nb_cols_before_split_sheets"])
        self.cols_total = QLineEdit(None, validator=QIntValidator(), text=self.settings_json["TABLE"]["nb_cols_total_head"])
        self.col_ID = QLineEdit(None, validator=QIntValidator(), text=self.settings_json["TABLE"]["col_ID"])
        self.col_date = QLineEdit(None, validator=QIntValidator(), text=self.settings_json["TABLE"]["col_date"])
        self.col_type = QLineEdit(None, validator=QIntValidator(), text=self.settings_json["TABLE"]["col_type"])

        table_settings_layout.addRow("Worksheet index:", self.index_worksheets)
        table_settings_layout.addRow("Row edit:", self.row_edit)
        table_settings_layout.addRow("Row head:", self.row_head)
        table_settings_layout.addRow("Cols before split:", self.cols_before_split)
        table_settings_layout.addRow("Cols total:", self.cols_total)
        table_settings_layout.addRow("Col ID:", self.col_ID)
        table_settings_layout.addRow("Col date:", self.col_date)
        table_settings_layout.addRow("Col type:", self.col_type)

        table_settings_group.setLayout(table_settings_layout)
        layout.addWidget(table_settings_group)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_button_clicked)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_button_clicked(self):
        index_worksheet = self.index_worksheets
        row_edit = self.row_edit
        row_head = self.row_head
        cols_before_split = self.cols_before_split
        cols_total = self.cols_total
        col_ID = self.col_ID
        col_date = self.col_date
        col_type = self.col_type

    def save_settings(self, data: dict):
        with open("configs/settings.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_settings(self) -> dict:
        with open("configs/settings.json", "r") as f:
            settings = json.load(f)
            return self.convert_to_str(settings)

    def convert_to_str(self, settings: dict) -> dict:
        str_settings = {}
        for key, value in settings.items():
            if isinstance(value, dict):
                str_settings[key] = self.convert_to_str(value)
            else:
                str_settings[key] = str(value)
        return str_settings
