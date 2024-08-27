from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSlot
from database import get_user

class LoginPage(QWidget):
    def __init__(self, switch_page_callback):
        super().__init__()
        self.switch_page_callback = switch_page_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Email Id')
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)

        self.signup_button = QPushButton('Sign Up', self)
        self.signup_button.clicked.connect(lambda: self.switch_page_callback(2))

        self.forgot_password_button = QPushButton('Forgot Password', self)
        self.forgot_password_button.clicked.connect(lambda: self.switch_page_callback(3))

        layout.addWidget(QLabel('Login'))
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.signup_button)
        layout.addWidget(self.forgot_password_button)
        self.setLayout(layout)

    @pyqtSlot()
    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        user = get_user(email, password)
        
        if user:
            self.switch_page_callback(1)  # Switch to home page
        else:
            # Display error message
            print("Invalid email or password\nemail-",email,'\npassword-',password)
