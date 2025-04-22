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
    QGridLayout,
    QGroupBox,
    QFormLayout
)
from PyQt5.QtGui import QIcon #type: ignore
from PyQt5.QtCore import Qt #type: ignore
# =============== GLOBALS ===============

# gets the location of the file so icon can be applied correctly
icon_path = os.path.join(os.path.dirname(__file__), "icon/onlinz_logo")

# =============== MAIN WINDOW ===============
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # sets basic window properties
        self.setWindowTitle("Onlinz Return Calculator")
        self.setMinimumSize(600, 400)
        self.setWindowIcon(QIcon(icon_path))
        
        # for managing different pages
        self.Stack = QStackedWidget(self)
        
        # creating empty pages
        self.customer_details_stack = QWidget()
        self.box_dimensions_stack = QWidget()
        self.customer_receipt_stack = QWidget()
        
        # initializing those pages
        self.customer_details_ui()
        self.box_dimensions_ui()
        self.customer_receipt_ui()
        
        # adds pages to stacked widgets
        self.Stack.addWidget(self.customer_details_stack)
        self.Stack.addWidget(self.box_dimensions_stack)
        self.Stack.addWidget(self.customer_receipt_stack)
        
        # sets where the stack widget will be displayed
        self.setCentralWidget(self.Stack)
        
    def customer_details_ui(self):
        # sets up form layout on customer details page
        layout = QFormLayout(self)
        self.customer_details_stack.setLayout(layout)
        
        # groups input fields under customer details
        customer_detailsbox = QGroupBox("Customer Details")
        
        # creates form layout for allowing simple addition of input fields
        form_layout = QFormLayout()
        customer_detailsbox.setLayout(form_layout)
        
        # Input fields for customer details - sets up two columns
        form_layout.addRow("First Name:", QLineEdit(customer_detailsbox))
        form_layout.addRow("Last Name:", QLineEdit(customer_detailsbox))
        form_layout.addRow("Email:", QLineEdit(customer_detailsbox))
        form_layout.addRow("Telephone Number:", QLineEdit(customer_detailsbox))
        form_layout.addRow("Address:", QLineEdit(customer_detailsbox))
        
        # adds customer_detailsbox to layout - this is needed to display UI
        layout.addWidget(customer_detailsbox)
  
    def box_dimensions_ui(self):
        pass
        
    def customer_receipt_ui(self):
        pass

# =============== APP INITIALIZATION ===============
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Applies stylesheet 
    with open('styles/style.qss', 'r') as f:
        style = f.read()
    app.setStyleSheet(style)
    # display main window
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())