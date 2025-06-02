# ONLINZ Return App

A PyQt5-based return shipping calculator for the ONLINZ e-commerce platform

 - *This program is developed as my school python project*

## 📜 Project Overview

This application was developed as part of the AS91896 New Zealand Digitial Technologies standard *Use advanced programming techniques to develop a computer
program*. It is front-end only, uses the PyQt5 GUI framework and Nord color scheme, uses regex and external modules for user validation and stacks as different pages. Includes customer details page, box dimensions page and a customer receipt page.

### Problem Statement

ONLINZ is a new online shopping website serving customers throughout New Zealand. All products are delivered free from their Auckland warehouse, allowing customers to try items before committing to purchase. If items are returned undamaged within 30 days, customers receive a full refund of the purchase price.

The only cost to customers is the courier return fee, which varies based on:
- **Location**: Customer's address within New Zealand
- **Package Size**: Dimensions of the return box

## 💡 Features

- **GUI Interface**: PyQt5 GUI Framework—Modern and user friendly with Nord color scheme
- **Validation**: Utilizes regex and external modules such as `phonenumbers` and `email_validator` for user input validation 
- **Customer Details**: Customer can enter their details: `first name`, `last name`, `email`, `telephone number`, `address`, `island`
- **Box Dimensions**: Allows user to enter box height, width and depth; this can be changed using buttons or editing directly
- **Customer Receipt**: Displays `Name`, `Email`, `Telephone Number`, `Address`, `Island Return`, `Box Volume` and `Cost of returning product`

## ⚙️ Installation

### Option 1: Download Pre-built Release

1. Visit the [Releases page](../../releases)
2. **For Executable `Windows Only`**: Download `Onlinz.exe` (ready to run)
3. **For Source code**: Download source code folder
   - `.zip` file for Windows
   - `.tar.gz` file for macOS and Linux
   -  Extract the archive and run `main.py`

### Option 2: Clone Repository

```bash
git clone https://github.com/dibxy/onlinz-return-app.git
cd onlinz-return-app
python main.py
```

### Manual Dependency Installation

If automatic dependency installation fails:

```bash
# create virtual environment
python -m venv venv

# activate virtual environment
source venv/bin/activate	# Linux/macOS
# OR
venv\Scripts\activate   	# Windows

# Install dependencies
pip install -r requirements.txt
```
## 💻 Usage

1. Launch the application by running `main.py` or the executable
2. Enter required customer details
3. Enter box dimensions
4. View calculated return shipping cost

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Developed for my NCEA Level 2 AS91896 Use advanced programming techniques to develop a computer program standard*
