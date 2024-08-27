from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSlot
from database import add_user

class SignupPage(QWidget):
    def __init__(self, switch_page_callback):
        super().__init__()
        self.switch_page_callback = switch_page_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Email Id')
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Name')
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Create new Password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.reenter_password_input = QLineEdit(self)
        self.reenter_password_input.setPlaceholderText('Reenter new Password')
        self.reenter_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.create_account_button = QPushButton('Create Account', self)
        self.create_account_button.clicked.connect(self.handle_signup)

        layout.addWidget(QLabel('Sign Up'))
        layout.addWidget(self.email_input)
        layout.addWidget(self.name_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.reenter_password_input)
        layout.addWidget(self.create_account_button)
        self.setLayout(layout)

    @pyqtSlot()
    def handle_signup(self):
        email = self.email_input.text()
        name = self.name_input.text()
        password = self.password_input.text()
        reentered_password = self.reenter_password_input.text()

        if password == reentered_password:
            result = add_user(name, email, password)
            if result == "account created successfully":
                self.switch_page_callback(0)  # Switch to login page
            else:
                # Display error message
                print(result)
        else:
            # Display error message
            print("Passwords do not match")
