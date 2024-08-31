from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSlot
from database import get_user, update_session_token
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
import uuid #importing for token generation
import sys
import os

class LoginPage(QWidget):
    def __init__(self, switch_page_callback, set_user_data):
        super().__init__()
        self.switch_page_callback = switch_page_callback
        self.set_user_data = set_user_data
        self.initUI()

    def initUI(self):

        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        illustrationpath = os.path.join(base_path, 'images', 'homepageillustration25-modified-small.png')
        logopath = os.path.join(base_path, 'images', 'homepagelogo.png')
        # Set Source Sans Pro font for the entire widget
        self.setFont(QFont("Source Sans Pro", 12))

        # Main layout: split into left (image) and right (login form)
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)
        # Left section: Image
        left_layout = QVBoxLayout()
        illustration_label = QLabel(self)
        illustration_pixmap = QPixmap(illustrationpath)  # Adjust path as needed
        illustration_label.setPixmap(illustration_pixmap)
        illustration_label.setScaledContents(True)
        illustration_label.setFixedSize(329, 365)
        left_layout.addWidget(illustration_label)

        # Right section: Login Form
        right_layout = QVBoxLayout()
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(logopath)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(184, 82)
        right_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        # Welcome label
        welcome_label = QLabel("Welcome to CueYou!")
        welcome_label.setFont(QFont('Source Sans Pro', 24))
        welcome_label.setStyleSheet("color: #1D263B; padding: 5px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(welcome_label)
        # Subtitle Text
        subtitle_label = QLabel("Login to Start Your Journey to Success", self)
        subtitle_label.setFont(QFont("Source Sans Pro", 14))
        subtitle_label.setStyleSheet("color: #1D263B")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(subtitle_label)
        # Email input
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Email Id')
        self.email_input.setFont(QFont("Source Sans Pro", 14))
        self.email_input.setStyleSheet("""
            QLineEdit {
                color: #1D263B;
                border: 0.5px solid #B2B2B2;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit::placeholder {
                color: #B2B2B2;  /* Placeholder text color */
            }                           
            """)
        right_layout.addWidget(self.email_input)
        # Password input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setFont(QFont("Source Sans Pro", 14))
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 0.5px solid #B2B2B2;
                color: #1D263B;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit::placeholder {
                color: #B2B2B2;  /* Placeholder text color */
            }
            """)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        right_layout.addWidget(self.password_input)
        # Forgot Password Link
        forgot_password_button = QLabel('<a href="#" style="color: #B2B2B2;">Forgot Password?</a>', self)
        forgot_password_button.setOpenExternalLinks(False)
        forgot_password_button.setFont(QFont("Source Sans Pro", 11))
        forgot_password_button.setStyleSheet("color: #1D263B")
        forgot_password_button.linkActivated.connect(lambda: self.switch_page_callback(4))
        right_layout.addWidget(forgot_password_button)
        # Login Button
        self.login_button = QPushButton('Login', self)
        self.login_button.setFont(QFont("Source Sans Pro", 12))
        self.login_button.setStyleSheet("padding: 8px; background-color: #003C8A; color: white; border-radius: 15px;")
        self.login_button.clicked.connect(self.handle_login)
        right_layout.addWidget(self.login_button)
        # Error Label
        self.error_label = QLabel('', self)
        self.error_label.setStyleSheet("color: red;")
        right_layout.addWidget(self.error_label)
        # Sign Up Link
        signup_link = QLabel("Don't have an account? <a href='#'>Sign up now!</a>", self)
        signup_link.setStyleSheet("color: #003C8A;")
        signup_link.setOpenExternalLinks(False)
        signup_link.linkActivated.connect(lambda: self.switch_page_callback(3))
        right_layout.addWidget(signup_link)

        # Add right layout to main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def save_token_to_file(self, token):
        with open('session_token.txt', 'w') as file:
            file.write(token)

    @pyqtSlot()
    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        user = get_user(email, password)
        
        if user:
            # Modified: Generate and update session token
            self.set_user_data(user)
            session_token = str(uuid.uuid4())
            update_session_token(user['userid'], session_token)  # Save token to the database
            self.save_token_to_file(session_token)  # Save token to a file
            self.switch_page_callback(0)  # Switch to home page
        else:
            # Display error message
            self.error_label.setText("Invalid email or password") 
            print("Invalid email or password\nemail-",email,'\npassword-',password)
