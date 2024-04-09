from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QSpacerItem, QSizePolicy, QFileDialog, QDialog, QGroupBox, QCheckBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
import json


class FileExplorerLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.openFileExplorer()

    def openFileExplorer(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier Excel", "", "Tous les fichiers (*)")
        if file_path:
            self.setText(file_path)


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

        self.excel_version = QCheckBox()
        self.sheets_version = QCheckBox()
        self.delta_version = QCheckBox()
        self.time_version = QCheckBox()

        versions_settings_layout.addRow("Excel version:", self.excel_version)
        versions_settings_layout.addRow("Sheets version:", self.sheets_version)
        versions_settings_layout.addRow("Delta:", self.delta_version)
        versions_settings_layout.addRow("Time", self.time_version)

        versions_settings_group.setLayout(versions_settings_layout)
        layout.addWidget(versions_settings_group)

        table_settings_group = QGroupBox("Table Settings")
        table_settings_layout = QFormLayout()

        self.index_worksheet = QLineEdit(None, validator=QIntValidator())
        self.row_edit = QLineEdit(None, validator=QIntValidator())
        self.row_head = QLineEdit(None, validator=QIntValidator())
        self.cols_before_split = QLineEdit(None, validator=QIntValidator())
        self.cols_total = QLineEdit(None, validator=QIntValidator())
        self.col_ID = QLineEdit(None, validator=QIntValidator())
        self.col_date = QLineEdit(None, validator=QIntValidator())
        self.col_type = QLineEdit(None, validator=QIntValidator())

        table_settings_layout.addRow("Worksheet index:", self.index_worksheet)
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
        index_worksheet = self.index_worksheet
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
            return json.load(f)


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.settings_json = self.load_settings()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("LiveSplit Server")

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Config ip + port
        config_group = QGroupBox("Configuration")
        config_layout = QFormLayout()

        self.server_ip = QLineEdit()
        self.port = QLineEdit()

        config_layout.addRow("Server IP:", self.server_ip)
        config_layout.addRow("Port:", self.port)
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        # OU
        table_group = QGroupBox("Ou ?")
        table_layout = QFormLayout()

        self.excel = FileExplorerLineEdit()
        self.sheets = QLineEdit()

        table_layout.addRow("Fichier Excel:", self.excel)
        table_layout.addRow("Sheet ID:", self.sheets)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)

        # Save
        save_layout = QFormLayout()

        save_button = QPushButton("Sauvegarde")
        save_button.clicked.connect(self.save_button_clicked)

        save_layout.addRow(save_button)
        layout.addLayout(save_layout)

        # SE CONNECTER
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        connect_button = QPushButton("SE CONNECTER")
        connect_button.setStyleSheet("background-color: green; color: white;")
        connect_button.setFixedSize(200, 50)
        button_layout.addWidget(connect_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Sttings button
        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings)
        layout.addWidget(settings_button)

        self.setLayout(layout)

    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()

    def save_button_clicked(self):
        server_ip = self.server_ip.text()
        port = int(self.port.text())
        excel = self.excel.text()
        sheets = self.sheets.text()

        print("server ip", server_ip)
        print("port", port)
        print("excel", excel)
        print("sheets", sheets)

    def save_settings(self, data: dict):
        with open("configs/settings.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_settings(self) -> dict:
        with open("configs/settings.json", "r") as f:
            return json.load(f)


app = QtWidgets.QApplication([])
win = App()
win.resize(800, 600)
win.show()
app.exec()
