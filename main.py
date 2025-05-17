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
    QFormLayout,
    QComboBox,
)
from PyQt5.QtGui import QIcon #type: ignore
from PyQt5.QtCore import Qt #type: ignore
# =============== GLOBALS ====s===========

# gets the location of the file so icon can be applied correctly
icon_path = os.path.join(os.path.dirname(__file__), "icon/onlinz_logo")

# =============== CONSTANTS ==============
# will be used for island select.
ISLANDS = ["North Island", "South Island", "Stewart Island"]

# =============== MAIN WINDOW ===============
class MainWindow(QMainWindow):
    """Main window of app manages stacked pages | customer details, 
    box dimensions and customer receipt."""
    def __init__(self):
        """Initializes main window"""
        super().__init__()
        # sets basic window properties
        self.setWindowTitle("Onlinz Return Calculator")
        self.setMinimumSize(450, 300)
        self.setWindowIcon(QIcon(icon_path))
        
        # for managing different pages
        self.Stack = QStackedWidget(self)
        
        # creating empty pages
        self.customer_details_stack = QWidget()
        self.box_dimensions_stack = QWidget()
        self.customer_receipt_stack = QWidget()
        
        # initializing customer details page
        self.customer_details_ui()
        
        # adds pages to stacked widgets
        self.Stack.addWidget(self.customer_details_stack)
        self.Stack.addWidget(self.box_dimensions_stack)
        self.Stack.addWidget(self.customer_receipt_stack)
        
        # sets where the stack widget will be displayed
        self.setCentralWidget(self.Stack)
        
    def customer_details_ui(self):
        """customer details page"""
        # sets up form layout on customer details page
        layout = QFormLayout()
        self.customer_details_stack.setLayout(layout)
        
        # groups input fields under customer details
        customer_detailsbox = QGroupBox("Customer Details")
        
        # creates form layout for allowing simple addition of input fields
        form_layout = QFormLayout()
        customer_detailsbox.setLayout(form_layout)
        
        #Initialize input variables
        self.first_name_input = QLineEdit(customer_detailsbox)
        self.last_name_input = QLineEdit(customer_detailsbox)
        self.email_input = QLineEdit(customer_detailsbox)
        self.telephone_input = QLineEdit(customer_detailsbox)
        self.address_input = QLineEdit(customer_detailsbox)
        self.island_select = QComboBox(customer_detailsbox)
        
        # add each island from the island list into the island select box
        for island in ISLANDS:
            self.island_select.addItem(island)
        
        # adds functionality to the next button to save the customer detials
        self.next_button = QPushButton("Next", customer_detailsbox)
        self.next_button.clicked.connect(self.save_customer_detail)
        
        # Input fields for customer details - sets up two columns
        form_layout.addRow("First Name:", self.first_name_input)
        form_layout.addRow("Last Name:", self.last_name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Telephone Number:", self.telephone_input)
        form_layout.addRow("Address:", self.address_input)
        form_layout.addRow("Island:", self.island_select)
        form_layout.addRow(self.next_button)
        
        # adds customer_detailsbox to layout - this is needed to display UI
        layout.addWidget(customer_detailsbox)
    
    def save_customer_detail(self):
        """customer inputted details are stored in this dictionary"""
        self.customer_details = {
            "first_name": self.first_name_input.text().capitalize(),
            "last_name": self.last_name_input.text().capitalize(),
            "email": self.email_input.text(),
            "telephone": self.telephone_input.text(),
            "address": self.address_input.text().title(),
            "island": self.island_select.currentText()
        }
        
        print("Customer Details:", self.customer_details)
        # change window to customer details page
        self.box_dimensions_ui()
        self.Stack.setCurrentIndex(1)
        
  
    def box_dimensions_ui(self):
        """box dimensions page"""
        # sets up form layout on box dimensions page
        layout = QFormLayout()
        self.box_dimensions_stack.setLayout(layout)
        
        # makes the title of the group the user's firts name's box dimensions
        first_name = self.customer_details.get("first_name")
        box_dimensionsbox = QGroupBox(f"{first_name}'s Box Dimensions")
        
        # creates form layout for allowing simple addition of input fields
        form_layout = QFormLayout()
        box_dimensionsbox.setLayout(form_layout)
        
        # Initialize input variables
        self.box_height_input = QLineEdit(box_dimensionsbox)
        self.box_width_input = QLineEdit(box_dimensionsbox)
        self.box_depth_input = QLineEdit(box_dimensionsbox)
        
        # the functionality for the back and next buttons
        self.next_button = QPushButton("Next", box_dimensionsbox)
        self.next_button.clicked.connect(self.save_box_dimension)
        self.back_button = QPushButton("Back", box_dimensionsbox)
        self.back_button.clicked.connect(lambda: self.Stack.setCurrentIndex(0))
        
        # adds input fields
        form_layout.addRow("Box Height:", self.box_height_input)
        form_layout.addRow("Box Width:", self.box_width_input)
        form_layout.addRow("Box Depth:", self.box_depth_input)
        form_layout.addRow(self.next_button)
        form_layout.addRow(self.back_button)
        
        # adds box_dimensionsbox to layout - this is needed to display UI
        layout.addWidget(box_dimensionsbox)
    
    def save_box_dimension(self):
        """customer inputted details for box dimensions are stored in this dictionary"""
        self.box_dimensions = {
            "box_height": float(self.box_height_input.text()),
            "box_width": float(self.box_width_input.text()),
            "box_depth": float(self.box_depth_input.text()),
        }
        
        print("Box Dimensions:", self.box_dimensions)
        # change window to customer receipt page
        self.Stack.setCurrentIndex(2)
        self.customer_receipt_ui()
        
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