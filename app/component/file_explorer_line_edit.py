from PySide6.QtWidgets import QLineEdit, QFileDialog
from PySide6.QtCore import Qt


class FileExplorerLineEdit(QLineEdit):
    def __init__(self, parent=None, text=""):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setText(text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.openFileExplorer()

    def openFileExplorer(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier Excel", "", "Tous les fichiers (*)")
        if file_path:
            self.setText(file_path)
