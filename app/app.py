from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox
from PySide6.QtGui import QIcon
import threading
import json

from app.component.file_explorer_line_edit import FileExplorerLineEdit
from app.component.settings_dialog import SettingsDialog


class App(QtWidgets.QWidget):
    main_loop_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.settings_json = self.load_settings()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("LiveSplit Server")
        self.setWindowIcon(QIcon('app/images/LiveSplit_ico.ico'))

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Config ip + port
        config_group = QGroupBox("Configuration")
        config_layout = QFormLayout()

        self.server_ip = QLineEdit(text=self.settings_json["SERVER"]["SERVER_IP"])
        self.port = QLineEdit(text=self.settings_json["SERVER"]["PORT"])

        config_layout.addRow("Server IP:", self.server_ip)
        config_layout.addRow("Port:", self.port)
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        # OU
        table_group = QGroupBox("Ou ?")
        table_layout = QFormLayout()

        self.excel = FileExplorerLineEdit(text=self.settings_json["PATH"]["path_excel"])
        self.sheets = QLineEdit(text=self.settings_json["PATH"]["sheet_id"])

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
        connect_button.clicked.connect(self.connect_button)
        connect_button.setStyleSheet("background-color: green; color: white;")
        connect_button.setFixedSize(200, 50)
        button_layout.addWidget(connect_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # TODO Button deconnect

        # Sttings button
        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings)
        layout.addWidget(settings_button)

        self.setLayout(layout)

    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()

    def save_button_clicked(self):
        self.settings_json["SERVER"]["SERVER_IP"] = self.server_ip.text()
        self.settings_json["SERVER"]["PORT"] = int(self.port.text())
        self.settings_json["PATH"]["path_excel"] = self.excel.text()
        self.settings_json["PATH"]["sheet_id"] = self.sheets.text()

        self.save_settings(self.settings_json)

    def connect_button(self):
        # TODO Problème fais "crash" l'app car fais tourner la loop. Le faire tourner en background
        self.main_loop_signal.emit()


    @staticmethod
    def save_settings(data: dict):
        with open("app/configs/settings.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_settings(self) -> dict:
        with open("app/configs/settings.json", "r") as f:
            settings = json.load(f)
            return self.convert_to_str(settings)

    def convert_to_str(self, settings: dict) -> dict:
        str_settings = {}
        for key, value in settings.items():
            if key in ["SERVER", "PATH"]:
                if isinstance(value, dict):
                    str_settings[key] = {k: str(v) for k, v in value.items()}
                else:
                    str_settings[key] = str(value)
            elif isinstance(value, dict):
                str_settings[key] = self.convert_to_str(value)
            else:
                str_settings[key] = value
        return str_settings
