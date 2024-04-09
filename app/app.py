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

        versions_settings_layout.addRow("Excel version:", QCheckBox())
        versions_settings_layout.addRow("Sheets version:", QCheckBox())
        versions_settings_layout.addRow("Delta:", QCheckBox())
        versions_settings_layout.addRow("Time", QCheckBox())

        versions_settings_group.setLayout(versions_settings_layout)
        layout.addWidget(versions_settings_group)

        table_settings_group = QGroupBox("Table Settings")
        table_settings_layout = QFormLayout()

        table_settings_layout.addRow("Worksheet index:", QLineEdit(None, validator=QIntValidator()))
        table_settings_layout.addRow("Row edit:", QLineEdit(None, validator=QIntValidator()))
        table_settings_layout.addRow("Row head:", QLineEdit(None, validator=QIntValidator()))
        table_settings_layout.addRow("Cols before split:", QLineEdit(None, validator=QIntValidator()))
        table_settings_layout.addRow("Cols total:", QLineEdit(None, validator=QIntValidator()))
        table_settings_layout.addRow("Col ID:", QLineEdit(None, validator=QIntValidator()))
        table_settings_layout.addRow("Col date:", QLineEdit(None, validator=QIntValidator()))
        table_settings_layout.addRow("Col type:", QLineEdit(None, validator=QIntValidator()))

        table_settings_group.setLayout(table_settings_layout)
        layout.addWidget(table_settings_group)

        layout.addWidget(QPushButton("Save"))

        self.setLayout(layout)

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
        config_layout.addRow("Server IP:", QLineEdit())
        config_layout.addRow("Port:", QLineEdit())
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        # OU
        table_group = QGroupBox("Ou ?")
        table_layout = QFormLayout()
        table_layout.addRow("Fichier Excel:", FileExplorerLineEdit())
        table_layout.addRow("Sheet ID:", QLineEdit())
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)

        # Save
        save_layout = QFormLayout()

        save_layout.addRow(QPushButton("Sauvegarde"))
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
