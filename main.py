import threading

from PySide6 import QtWidgets
from PySide6.QtGui import QIcon

from app.app import App
from thread_main import main


def run_thread_main():
    thread_main_loop = threading.Thread(target=main)
    thread_main_loop.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QIcon('app/images/LiveSplit_ico.ico'))
    win = App()
    win.resize(800, 600)
    win.show()
    win.main_loop_signal.connect(run_thread_main)
    app.exec()
