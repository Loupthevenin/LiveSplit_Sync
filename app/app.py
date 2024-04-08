from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QSpacerItem, QSizePolicy, QFileDialog
from PySide6.QtCore import Qt


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


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("LiveSplit Server")

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # 1) Title
        title_network_label = QLabel("Configuration")
        title_network_label.setMaximumHeight(50)
        layout.addWidget(title_network_label)

        form_layout = QFormLayout()

        # IP
        ip_label = QLabel("Server IP:")
        ip_textbox = QLineEdit()
        ip_textbox.setMaximumWidth(100)
        form_layout.addRow(ip_label, ip_textbox)
        # PORT
        port_label = QLabel("Port:")
        port_textbox = QLineEdit()
        port_textbox.setMaximumWidth(100)
        form_layout.addRow(port_label, port_textbox)

        layout.addLayout(form_layout)

        # Excel
        excel_path_label = QLabel("Fichier Excel:")
        file_textbox = FileExplorerLineEdit()
        file_textbox.setMaximumWidth(400)
        form_layout.addRow(excel_path_label)
        form_layout.addRow(file_textbox)

        # Sheets
        sheet_id_label = QLabel("Sheet ID:")
        sheet_id_textbox = QLineEdit()
        sheet_id_textbox.setMaximumWidth(400)
        form_layout.addRow(sheet_id_label)
        form_layout.addRow(sheet_id_textbox)

        # Save
        save_button = QPushButton("Sauvegarde")
        save_button.setFixedSize(80, 40)
        form_layout.addRow(save_button)

        # SE CONNECTER
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        connect_button = QPushButton("SE CONNECTER")
        connect_button.setStyleSheet("background-color: green; color: white;")
        connect_button.setFixedSize(200, 50)
        button_layout.addWidget(connect_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_config(self):
        pass


app = QtWidgets.QApplication([])
win = App()
win.resize(800, 600)
win.show()
app.exec()
