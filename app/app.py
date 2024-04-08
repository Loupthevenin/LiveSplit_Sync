import random
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QLineEdit, QLabel, QPushButton, QVBoxLayout


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Auto Split")

        # Wdgets creation
        self.textbox_ip = QLineEdit(self)
        self.textbox_port = QLineEdit(self)

        # Creation layout
        layout = QVBoxLayout()
        layout.addWidget(self.textbox_ip)
        layout.addWidget(self.textbox_port)

        self.setLayout(layout)


app = QtWidgets.QApplication([])
win = App()
win.resize(800, 600)
win.show()
app.exec()
