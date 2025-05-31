# Onlinz return calculator app

# =============== IMPORTS ===============
import sys
import os
import re
import subprocess
import phonenumbers
from email_validator import validate_email
from PyQt5.QtWidgets import (  # type: ignore
    QApplication,
    QMainWindow,
    QWidget,
    QStackedWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QGroupBox,
    QFormLayout,
    QComboBox,
    QDoubleSpinBox,
)
from PyQt5.QtGui import QIcon, QIntValidator #type: ignore

def install_dependencies():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print("requirements.txt not found. Please install dependencies manually or use Onlinz.exe")
        return
    try:
        print("Installing required dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
    except Exception:
        print("failed to install dependencies—check if pip is installed or use Onlinz.exe instead")
        sys.exit(1)

# =============== GLOBALS ===============
# gets the location of the file so icon can be applied correctly
icon_path = os.path.join(os.path.dirname(__file__), "icon/onlinz_logo")

# =============== CONSTANTS ==============
# will be used for island select and base multipler.
ISLANDS = {"North Island": 1, "South Island": 1.5, "Stewart Island": 2} 

# =============== MAIN WINDOW ===============
class MainWindow(QMainWindow):
    """Main window of app manages stacked pages | customer details, 
    box dimensions and customer receipt."""
    def __init__(self):
        """Initializes main window"""
        super().__init__()
        # sets basic window properties
        self.setWindowTitle("Onlinz Return Calculator")
        self.setMinimumSize(475, 300)
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
        
# =============== LOGIC ===============   
    def calculate_base_rate(self, volume):
        """the base rate is calculted based on the box's volume""" 
        if volume <= 6000:
            return 8
        elif volume < 100000:
            return 12
        else:
            return 15
    
    def calculate_return_cost(self, volume, island):
        """the return cost is calculated based on the base rate and which island the box will be returned to"""
        base_rate = self.calculate_base_rate(volume)
        base_multiplier = ISLANDS[island]
        return base_rate * base_multiplier
    
    def name_verify(self, first_name, last_name):
        """verify's the first and last name using regex"""
        name_regex = re.compile(
                r"""^
                [A-Za-zÀ-ÿ]                             # must start with a letter
                [A-Za-zÀ-ÿ\s'’-]{0,80}                  # allow up to 80 characters
                $""",
                re.UNICODE | re.VERBOSE
            )
        first_valid = bool(name_regex.fullmatch(first_name))
        last_valid = bool(name_regex.fullmatch(last_name))
        return first_valid, last_valid
    
    def email_verify(self, email):
        """verify's the email address using email_validator"""
        allowed_domains = ["example.com", "example.org", "example.net"]
        try:
            validate_email(email)
            return True
        except Exception:
            domain = email.split('@')[-1].lower()
            if domain in allowed_domains:
                return True
            return False
    
    def telephone_verify(self, telephone):
        """use phonenumbers library to verify if telephone is valid"""
        try:
            parsed = phonenumbers.parse(telephone, 'NZ')
            if phonenumbers.is_valid_number(parsed):
                return True
        except Exception:
            return False
    
    def address_verify(self, address):
        """veryify's how valid the address is using regex"""
        nz_address_regex = re.compile(
            r"""^
            (?P<number>\d{1,5}[A-Z]?(/\d{1,4})?)              # street number or unit
            \s+
            (?P<street>[A-Za-zÀ-ÿ\s'\-]+)                     # street name
            \s+
            (?P<type>Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr|
                Crescent|Cres|Terrace|Terr|Place|Pl|Way|Court|Ct|
                Parade|Pde|Quay|Rise|Square|Sq|Loop|Close|Cl|
                Highway|Hwy|Track|Trk|Esplanade|Esp)          # street type
            (?:,\s*(?P<suburb>[A-Za-zÀ-ÿ\s'\-]+))?            # optional suburb
            (?:,\s*(?P<city>[A-Za-zÀ-ÿ\s'\-]+))?              # optional city
            (?:\s+(?P<postcode>\d{4}))?                       # optional 4-digit postcode
            $""",
            re.IGNORECASE | re.VERBOSE
        )
        if re.match(nz_address_regex, address) is not None:
            return True
        else:
            return False
    
    def toggle_customer_button(self):
            """confirms if there is valid input in all customer details before permitting next"""
            # customer detail input
            first = self.first_name_input.text().strip()
            last = self.last_name_input.text().strip()
            email = self.email_input.text().strip()
            telephone = self.telephone_input.text().strip()
            address = self.address_input.text().strip()

            # verify if entries are valid
            first_valid, last_valid = self.name_verify(first, last)
            email_valid = self.email_verify(email)
            telephone_valid = self.telephone_verify(telephone)
            address_valid = self.address_verify(address)

            # show warning message when input is invalid 
            self.first_name_warning_message.setVisible(first != "" and not first_valid)
            self.last_name_warning_message.setVisible(last != "" and not last_valid)
            self.email_warning_message.setVisible(email != "" and not email_valid)
            self.telephone_warning_message.setVisible(telephone != "" and not telephone_valid)
            self.address_warning_message.setVisible(address != "" and not address_valid)

            # enable next button when all entries are filled and valid
            all_valid = [
                first != "" and first_valid,
                last != "" and last_valid,
                email != "" and email_valid,
                telephone != "" and telephone_valid,
                address != "" and address_valid,
            ]
            self.customer_next_button.setEnabled(all(all_valid))
            
    def toggle_box_button(self):
        """checks if all input fields have entries then if true enables next button"""
        dimensions = [
            self.box_height_input.text().strip(),
            self.box_width_input.text().strip(),
            self.box_depth_input.text().strip()
        ]
        self.box_next_button.setEnabled(all(dimensions))

# =============== CUSTOMER DETAILS PAGE =============== 
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
        for island in ISLANDS.keys():
            self.island_select.addItem(island)
        
        # restrict telephone input
        telephone_validator = QIntValidator(customer_detailsbox)
        self.telephone_input.setValidator(telephone_validator)
        
        # name warning message
        self.first_name_warning_message = QLabel("Name must only contain letters, spaces, hyphens, or apostrophes", customer_detailsbox)
        self.first_name_warning_message.setStyleSheet("color: red")
        self.first_name_warning_message.setVisible(False)
        
        self.last_name_warning_message = QLabel("Name must only contain letters, spaces, hyphens, or apostrophes", customer_detailsbox)
        self.last_name_warning_message.setStyleSheet("color: red")
        self.last_name_warning_message.setVisible(False)
        
        # email warning message
        self.email_warning_message = QLabel("Please enter a valid email address", customer_detailsbox)
        self.email_warning_message.setStyleSheet("color: red")
        self.email_warning_message.setVisible(False)
        
        # telephone warning message
        self.telephone_warning_message = QLabel("Please enter a valid NZ telephone number", customer_detailsbox)
        self.telephone_warning_message.setStyleSheet("color: red")
        self.telephone_warning_message.setVisible(False)
        
        # address warning message
        self.address_warning_message = QLabel("Please enter a valid address", customer_detailsbox)
        self.address_warning_message.setStyleSheet("color: red")
        self.address_warning_message.setVisible(False)
        
        # checks if all input fields have an entry; when this is true the next button enabled
        self.first_name_input.textChanged.connect(self.toggle_customer_button)
        self.last_name_input.textChanged.connect(self.toggle_customer_button)
        self.email_input.textChanged.connect(self.toggle_customer_button)
        self.telephone_input.textChanged.connect(self.toggle_customer_button)
        self.address_input.textChanged.connect(self.toggle_customer_button)
        
        # adds functionality to the next button to save the customer detials
        self.customer_next_button = QPushButton("Next", customer_detailsbox)
        self.customer_next_button.clicked.connect(self.save_customer_detail)
        
        # Input fields and errors for customer details - sets up two columns
        form_layout.addRow("First Name:", self.first_name_input)
        form_layout.addRow("", self.first_name_warning_message)
        form_layout.addRow("Last Name:", self.last_name_input)
        form_layout.addRow("", self.last_name_warning_message)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("", self.email_warning_message) 
        form_layout.addRow("Telephone Number:", self.telephone_input)
        form_layout.addRow("", self.telephone_warning_message) 
        form_layout.addRow("Address:", self.address_input)
        form_layout.addRow("", self.address_warning_message) 
        form_layout.addRow("Island:", self.island_select)
        form_layout.addRow(self.customer_next_button)
        
        # disables next button
        self.customer_next_button.setEnabled(False)
        
        # adds customer_detailsbox to layout - this is needed to display UI
        layout.addWidget(customer_detailsbox)
    
    def save_customer_detail(self):
        """customer inputted details are stored in this dictionary"""
        
        self.customer_details = {
            "first_name": self.first_name_input.text().capitalize(),
            "last_name": self.last_name_input.text().capitalize(),
            "email": self.email_input.text().strip(),
            "telephone": self.telephone_input.text(),
            "address": self.address_input.text().title(),
            "island": self.island_select.currentText()
        }
    
        # change window to customer details page
        self.box_dimensions_ui()
        self.Stack.setCurrentIndex(1)
        
# =============== BOX DIMENSIONS PAGE ===============         
    def box_dimensions_ui(self):
        """box dimensions page"""
        # clear existing layout if existing
        if self.box_dimensions_stack.layout() is not None:
            QWidget().setLayout(self.box_dimensions_stack.layout())
            
        # sets up form layout on box dimensions page
        layout = QFormLayout()
        self.box_dimensions_stack.setLayout(layout)
        
        # makes the title of the group the user's first name's box dimensions
        first_name = self.customer_details.get("first_name")
        box_dimensionsbox = QGroupBox(f"{first_name}'s Box Dimensions")
        
        # creates form layout for allowing simple addition of input fields
        form_layout = QFormLayout()
        box_dimensionsbox.setLayout(form_layout)

        # restrict and validate box dimensions by creating a Spin box
        # box height
        self.box_height_input = QDoubleSpinBox(box_dimensionsbox)
        self.box_height_input.setRange(5, 100)
        self.box_height_input.setSuffix(" cm")
        self.box_height_input.setDecimals(2)
        # box width
        self.box_width_input = QDoubleSpinBox(box_dimensionsbox)
        self.box_width_input.setRange(5, 100)
        self.box_width_input.setSuffix(" cm")
        self.box_width_input.setDecimals(2)
        #box depth
        self.box_depth_input = QDoubleSpinBox(box_dimensionsbox)
        self.box_depth_input.setRange(5, 100)
        self.box_depth_input.setSuffix(" cm")
        self.box_depth_input.setDecimals(2)
        
        # checks if all input fields have an entry; when this is true the next button enabled
        self.box_height_input.valueChanged.connect(self.toggle_box_button)
        self.box_width_input.valueChanged.connect(self.toggle_box_button)
        self.box_depth_input.valueChanged.connect(self.toggle_box_button)
        
        # the functionality for the back and next buttons
        self.box_next_button = QPushButton("Next", box_dimensionsbox)
        self.box_next_button.clicked.connect(self.save_box_dimension)
        self.box_back_button = QPushButton("Back", box_dimensionsbox)
        self.box_back_button.clicked.connect(lambda: self.Stack.setCurrentIndex(0))
        
        # adds input fields
        form_layout.addRow("Box Height:", self.box_height_input)
        form_layout.addRow("Box Width:", self.box_width_input)
        form_layout.addRow("Box Depth:", self.box_depth_input)
        form_layout.addRow(self.box_next_button)
        form_layout.addRow(self.box_back_button)
        
        # disables next button
        self.box_next_button.setEnabled(False)
        
        # adds box_dimensionsbox to layout - this is needed to display UI
        layout.addWidget(box_dimensionsbox)
    
    def save_box_dimension(self):
        """customer inputted details for box dimensions are stored in this dictionary"""
        self.box_dimensions = {
            "box_height": float(self.box_height_input.value()),
            "box_width": float(self.box_width_input.value()),
            "box_depth": float(self.box_depth_input.value()),
        }
        
        # change window to customer receipt page
        self.customer_receipt_ui()
        self.Stack.setCurrentIndex(2)
        
# =============== CUSTOMER RECEIPT PAGE ===============         
    def customer_receipt_ui(self):
        """customer receipt page"""
        # clear existing layout if existing
        if self.customer_receipt_stack.layout() is not None:
            QWidget().setLayout(self.customer_receipt_stack.layout())
            
        # sets up form layout on customer receipt page
        layout = QFormLayout()
        self.customer_receipt_stack.setLayout(layout)
        
        # get the data from the customer details list
        first_name = self.customer_details.get("first_name")
        last_name = self.customer_details.get("last_name")
        email = self.customer_details.get("email")
        telephone = self.customer_details.get("telephone")
        address = self.customer_details.get("address")
        island = self.customer_details.get("island")
        
        # get the data from box dimensions list
        box_height = self.box_dimensions.get("box_height")
        box_width = self.box_dimensions.get("box_width")
        box_depth = self.box_dimensions.get("box_depth")
        
        # calculating box volume
        box_volume = box_height * box_width * box_depth
        
        # calculating return cost
        return_cost = self.calculate_return_cost(box_volume, island)
        
        # makes the title of the group the user's firts name's box dimensions
        customer_receipt_box = QGroupBox(f"{first_name}'s Receipt")
        
        # creates form layout for allowing simple addition of input fields
        form_layout = QFormLayout()
        customer_receipt_box.setLayout(form_layout)
        
        # Initialize input variables
        self.full_name_entry = QLabel(f"Name: {first_name} {last_name}")
        self.email_entry = QLabel(f"Email: {email}")
        self.telephone_entry = QLabel(f"Telephone: {telephone}")
        self.address_entry = QLabel(f"Address: {address}")
        self.island_entry = QLabel(f"Island Return: {island}")
        self.box_dimensions_entry = QLabel(f"Box Volume: {box_height}cm × {box_width}cm × {box_depth}cm = {box_volume:.2f}cm³")
        self.return_cost_total = QLabel(f"Cost of returning product: ${return_cost:.2f}")
        
        # adds functionality to the buttons
        self.finish_button = QPushButton("Finish", customer_receipt_box)
        self.finish_button.clicked.connect(lambda: sys.exit())
        
        self.back_button = QPushButton("Back", customer_receipt_box)
        self.back_button.clicked.connect(lambda: self.Stack.setCurrentIndex(1))
        
        # Display fields detailing customer reciept
        form_layout.addRow(self.full_name_entry)
        form_layout.addRow(self.email_entry)
        form_layout.addRow(self.telephone_entry)
        form_layout.addRow(self.address_entry)
        form_layout.addRow(self.island_entry)
        form_layout.addRow(self.box_dimensions_entry)
        form_layout.addRow(self.return_cost_total)
        form_layout.addRow(self.finish_button)
        form_layout.addRow(self.back_button)
        
        # adds box_dimensionsbox to layout - this is needed to display UI
        layout.addWidget(customer_receipt_box)

# =============== APP INITIALIZATION ===============
if __name__ == '__main__':
    install_dependencies()
    app = QApplication(sys.argv)
   # Applies stylesheet
    try:
        with open('styles/style.qss', 'r') as f:
            style = f.read()
        app.setStyleSheet(style)
    except Exception:
        print("Unable to apply stylesheet")
        print("Using application without stylesheet")
    # display main window
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())