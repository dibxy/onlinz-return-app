# Onlinz return calculator app

# =============== IMPORTS ===============
import sys
import os
from PyQt5.QtWidgets import (  # type: ignore
    QApplication,
    QMainWindow,
    QWidget,
    QStackedWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout, 
)
from PyQt5.QtGui import QIcon #type: ignore

# gets the location of the file so icon can be applied correctly
icon_path = os.path.join(os.path.dirname(__file__), "icon/onlinz_logo")

# sets up main window of the app
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Onlinz Return Calculator")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(icon_path))

# initilizes the app and applies stylesheet
if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open('styles/style.qss', 'r') as f:
        style = f.read()
    app.setStyleSheet(style)
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())