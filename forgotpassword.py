from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSlot

class ForgotPasswordPage(QWidget):
    def __init__(self, switch_page_callback):
        super().__init__()
        self.switch_page_callback = switch_page_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Enter Email Id')
        self.otp_input = QLineEdit(self)
        self.otp_input.setPlaceholderText('Enter OTP')
        self.new_password_input = QLineEdit(self)
        self.new_password_input.setPlaceholderText('Enter new Password')
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.reenter_password_input = QLineEdit(self)
        self.reenter_password_input.setPlaceholderText('Reenter new Password')
        self.reenter_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.send_otp_button = QPushButton('Send OTP', self)
        self.send_otp_button.clicked.connect(self.handle_send_otp)
        self.verify_otp_button = QPushButton('Verify OTP', self)
        self.verify_otp_button.clicked.connect(self.handle_verify_otp)
        self.change_password_button = QPushButton('Change Password', self)
        self.change_password_button.clicked.connect(self.handle_change_password)

        layout.addWidget(QLabel('Forgot Password'))
        layout.addWidget(self.email_input)
        layout.addWidget(self.send_otp_button)
        layout.addWidget(self.otp_input)
        layout.addWidget(self.verify_otp_button)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.reenter_password_input)
        layout.addWidget(self.change_password_button)
        self.setLayout(layout)

    @pyqtSlot()
    def handle_send_otp(self):
        email = self.email_input.text()
        # Validate email and send OTP
        pass

    @pyqtSlot()
    def handle_verify_otp(self):
        otp = self.otp_input.text()
        # Verify OTP
        pass

    @pyqtSlot()
    def handle_change_password(self):
        new_password = self.new_password_input.text()
        reentered_password = self.reenter_password_input.text()
        # Change password in MongoDB
        if new_password == reentered_password:
            self.switch_page_callback(0)  # Switch to login page
        else:
            # Display error message
            pass
