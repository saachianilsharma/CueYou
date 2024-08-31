from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QFont
from database import get_otp, update_password, delete_otp, get_user_by_email
from otp import send_otp
import hashlib
from PyQt6.QtCore import Qt
import re

class ForgotPasswordPage(QWidget):
    def __init__(self, switch_page_callback):
        super().__init__()
        self.switch_page_callback = switch_page_callback
        self.otp_sent = False  # Track if OTP was sent
        self.email_verified = False  # Track if OTP was verified
        self.initUI()

    def initUI(self):
         # Set Source Sans Pro font for the entire widget
        self.setFont(QFont("Source Sans Pro", 12))
        
        layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setStyleSheet("color: #1D263B;")
        self.email_input.setPlaceholderText('Enter Email Id')
        self.otp_input = QLineEdit(self)
        self.otp_input.setStyleSheet("color: #1D263B;")
        self.otp_input.setPlaceholderText('Enter OTP')
        self.new_password_input = QLineEdit(self)
        self.new_password_input.setStyleSheet("color: #1D263B;")
        self.new_password_input.setPlaceholderText('Enter new Password')
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.reenter_password_input = QLineEdit(self)
        self.reenter_password_input.setStyleSheet("color: #1D263B;")
        self.reenter_password_input.setPlaceholderText('Reenter new Password')
        self.reenter_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.send_otp_button = QPushButton('Send OTP', self)
        self.send_otp_button.setStyleSheet("""
            QPushButton {
                background-color: #003C8A;
                color: white;
                border-radius: 15px;
                padding: 5px 20px;
                font-size: 16px;
                
            }
            QPushButton:disabled {
                background-color: #B2B2B2;
            }
        """)
        self.send_otp_button.clicked.connect(self.handle_send_otp)
        self.verify_otp_button = QPushButton('Verify OTP', self)
        self.verify_otp_button.setStyleSheet("""
            QPushButton {
                background-color: #003C8A;
                color: white;
                border-radius: 15px;
                padding: 5px 20px;
                font-size: 16px;
                
            }
            QPushButton:disabled {
                background-color: #B2B2B2;
            }
        """)
        self.verify_otp_button.clicked.connect(self.handle_verify_otp)
        self.change_password_button = QPushButton('Change Password', self)
        self.change_password_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9F1C;
                color: white;
                border-radius: 15px;
                padding: 5px 20px;
                font-size: 16px;
                
            }
            QPushButton:disabled {
                background-color: #B2B2B2;
            }
        """)
        self.change_password_button.clicked.connect(self.handle_change_password)

        self.back_button = QPushButton("Back to Login")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #003C8A;
                color: white;
                border-radius: 15px;
                padding: 5px 20px;
                font-size: 16px;
            }
        """)
        self.back_button.clicked.connect(lambda: self.switch_page_callback(2)) # switch to login page

        self.error_label = QLabel("", self)
        self.error_label.setFont(QFont("Source Sans Pro", 12))
        self.error_label.setStyleSheet("color: red;")  # Style the error message in red
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Initially disable OTP and password fields until OTP is sent
        self.otp_input.setDisabled(True)
        self.verify_otp_button.setDisabled(True)
        self.new_password_input.setDisabled(True)
        self.reenter_password_input.setDisabled(True)
        self.change_password_button.setDisabled(True)
        # label 
        heading = QLabel('Forgot Password')
        heading.setFont(QFont('Source Sans Pro', 18))
        heading.setStyleSheet("color: #003C8A; padding: 5px; font-weight: bold;")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(heading)
        layout.addWidget(self.email_input)
        layout.addWidget(self.send_otp_button)
        layout.addWidget(self.otp_input)
        layout.addWidget(self.verify_otp_button)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.reenter_password_input)
        layout.addWidget(self.error_label)
        layout.addWidget(self.change_password_button)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    @pyqtSlot()
    def handle_send_otp(self):
        email = self.email_input.text().strip()
        # Validate email and send OTP
        user = get_user_by_email(email)
        if user:
            dbotp = get_otp(user.get("userid"))
            if dbotp is not None:
                delete_otp(user['userid'])
            else:
                success, message = send_otp(email)
                if success:
                    self.otp_sent = True
                    self.email_verified = True
                    self.otp_input.setEnabled(True)
                    self.verify_otp_button.setEnabled(True)
                    #QMessageBox.information(self, "Success", message)
                    print("Success ",message)
                else:
                    self.error_label.setText("Error - ", message)
                    print("Error ",message)
        else:
            self.error_label.setText("Invalid Email ID")
            print("Error ",message)
        

    @pyqtSlot()
    def handle_verify_otp(self):
        otp = self.otp_input.text()
        print("user inserted otp - ", otp)
        # Verify OTP
        email = self.email_input.text()
        user = get_user_by_email(email)
        dbotp = get_otp(user.get("userid"))
        print("otp from db - ", dbotp)
        if otp==dbotp:
            self.email_verified= True
            self.new_password_input.setEnabled(True)
            self.reenter_password_input.setEnabled(True)
            self.change_password_button.setEnabled(True)
            #QMessageBox.information(self, "Success", "OTP verified. You can now change your password.")
            print("OTP verified. You can now change your password.")
            delete_otp(user['userid'])  # Delete the OTP after successful password change
        else:
            self.error_label.setText("Invalid OTP. Please try again.")
            print("Error", "Invalid OTP. Please try again.")


    def validate_password(self,password):
        
        pattern = re.compile(
            r'^(?=.*[a-z])'          # At least one lowercase letter
            r'(?=.*[A-Z])'          # At least one uppercase letter
            r'(?=.*\d)'             # At least one digit
            r'(?=.*[@$!%*?&])'     # At least one special character
            r'.{8,}$'              # Minimum 8 characters
        )    
        return bool(pattern.match(password))
    
    @pyqtSlot()
    def handle_change_password(self):
        if not self.email_verified:
            self.error_label.setText("Error Please verify OTP first.")
            print("Error - Please verify OTP first.")
            return

        new_password = self.new_password_input.text()
        reentered_password = self.reenter_password_input.text()
        email = self.email_input.text().strip()

        if new_password == reentered_password:
            if not self.validate_password(new_password):
                self.error_label.setText("Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
            if self.validate_password(new_password):
                user = get_user_by_email(email)
                if user:
                    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                    update_password(user['userid'], hashed_password)
                    self.error_label.setText("Password changed successfully.")
                    self.error_label.setStyleSheet("color: #003C8A;")
                    print("Success", "Password changed successfully. Please proceed to login with your new Password.")
                else:
                    self.error_label.setText("Error", "An error occurred. Please try again.")
                    print("Error", "couldnt fetch user from db in handle_change_password()")