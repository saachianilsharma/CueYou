from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox,QFormLayout,QScrollArea, QHBoxLayout
from PyQt6.QtCore import pyqtSlot
from database import add_user
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import re
import sys 
import os 

class SignupPage(QWidget):
    def __init__(self, switch_page_callback):
        super().__init__()
        self.switch_page_callback = switch_page_callback
        self.initUI()

    def validate_password(self,password):
        
        pattern = re.compile(
            r'^(?=.*[a-z])'          # At least one lowercase letter
            r'(?=.*[A-Z])'          # At least one uppercase letter
            r'(?=.*\d)'             # At least one digit
            r'(?=.*[@$!%*?&])'     # At least one special character
            r'.{8,}$'              # Minimum 8 characters
        )    
        return bool(pattern.match(password))
    
    def initUI(self):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        # Set Source Sans Pro font for the entire widget
        self.setFont(QFont("Source Sans Pro", 12))
        self.setStyleSheet("color: #1D263B")
        # Sign up label
        signup_label = QLabel("Sign Up", self)
        signup_label.setFont(QFont("Source Sans Pro", 18))
        signup_label.setStyleSheet("color: #003C8A; font-weight: bold; ")
        # Email ID
        email_label = QLabel("Email", self)
        email_label.setFont(QFont("Source Sans Pro", 12))
        email_label.setStyleSheet("color: #1D263B")
        self.email_input = QLineEdit(self)
        self.email_input.setStyleSheet("""
            QLineEdit {
                color: #1D263B;            
                border: 0.5px solid #B2B2B2;
                padding: 5px;
                font-size: 12px;
            }""")
        self.email_input.setPlaceholderText('Email Id')
        # Name
        name_label = QLabel("Name", self)
        name_label.setFont(QFont("Source Sans Pro", 12))
        name_label.setStyleSheet("color: #1D263B")
        self.name_input = QLineEdit(self)
        self.name_input.setStyleSheet("""
            QLineEdit {
                color: #1D263B;
                border: 0.5px solid #B2B2B2;
                padding: 5px;
                font-size: 12px;
            }""")
        self.name_input.setPlaceholderText('Name')
        # Enter Password
        password_label = QLabel("Password", self)
        password_label.setFont(QFont("Source Sans Pro", 12))
        password_label.setStyleSheet("color: #1D263B")
        self.password_input = QLineEdit(self)
        self.password_input.setStyleSheet("""
            QLineEdit {
                color: #1D263B;
                border: 0.5px solid #B2B2B2;
                padding: 5px;
                font-size: 12px;
            }""")
        self.password_input.setPlaceholderText('Create new Password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        # Re enter Password
        reenterpassword_label = QLabel("Reenter Password", self)
        reenterpassword_label.setFont(QFont("Source Sans Pro", 12))
        reenterpassword_label.setStyleSheet("color: #1D263B")
        self.reenter_password_input = QLineEdit(self)
        self.reenter_password_input.setStyleSheet("""
            QLineEdit {
                color: #1D263B;
                border: 0.5px solid #B2B2B2;
                padding: 5px;
                font-size: 12px;
            }""")
        self.reenter_password_input.setPlaceholderText('Reenter new Password')
        self.reenter_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        # stylesheet for QComboBox
        
        arrowpath = os.path.join(base_path, 'images', 'black-arrow.png').replace("\\", "/")
        stylesheettext="""
            QComboBox {
                
                border-radius: 15px;
                padding: 5px 20px;
                font-size: 12px;
                background-color: white;
                color: #1D263B;
                
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
                color: #1D263B;
                background-color: white;
            }
            QComboBox::down-arrow {
                width: 10px;
                image: url("""+str(arrowpath)+""");
                height: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: white;  /* Background color of dropdown items */
                color: #1D263B;  /* Text color of dropdown items */
                selection-background-color: #003C8A;  /* Background color for selected item */
                selection-color: white;  /* Text color for selected item */
            }
        """
        # Country
        country_label = QLabel("Country", self)
        country_label.setFont(QFont("Source Sans Pro", 12))
        country_label.setStyleSheet("color: #1D263B")
        self.country_dropdown = QComboBox(self)
        self.country_dropdown.setStyleSheet(stylesheettext)
        self.country_dropdown.addItems([
            'Select Country', 'USA', 'India', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'Japan', 'Other'
        ])
        # Field of work
        fieldofwork_label = QLabel("Field of Work", self)
        fieldofwork_label.setFont(QFont("Source Sans Pro", 12))
        fieldofwork_label.setStyleSheet("color: #1D263B")
        self.field_of_work_dropdown = QComboBox(self)
        self.field_of_work_dropdown.setStyleSheet(stylesheettext)
        self.field_of_work_dropdown.addItems([
            'Select Field of Work', 'IT', 'Education', 'Finance', 'Healthcare', 'Engineering', 'Marketing', 'Sales', 'Other'
        ])
        # Position at Firm
        position_label = QLabel("Position", self)
        position_label.setFont(QFont("Source Sans Pro", 12))
        position_label.setStyleSheet("color: #1D263B")
        self.position_dropdown = QComboBox(self)
        self.position_dropdown.setStyleSheet(stylesheettext)
        self.position_dropdown.addItems(['Select Position', 'Managerial', 'Non-managerial','None / Fresher'])
        # Experience
        experience_label = QLabel("Experience", self)
        experience_label.setFont(QFont("Source Sans Pro", 12))
        experience_label.setStyleSheet("color: #1D263B")
        self.experience_dropdown = QComboBox(self)
        self.experience_dropdown.setStyleSheet(stylesheettext)
        self.experience_dropdown.addItems(['Select Experience', '0-2 years', '3-5 years', '6-10 years', '10+ years'])
        # Are you a student
        checkbox_layout = QHBoxLayout()
        self.student_checkbox = QCheckBox('Are you a student?', self)
        checkbox_layout.addWidget(self.student_checkbox)
        checkbox_layout.addStretch()
        self.student_checkbox.setFont(QFont("Source Sans Pro", 12))
        self.student_checkbox.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.student_checkbox.setStyleSheet("""
            QCheckBox {
                color: #1D263B;
                padding: 5px;
            }
            QCheckBox::indicator {
                border: 0.5px solid #1D263B;
            }
        """)
        checkbox_layout.addWidget(QLabel()) 
        # Purpose of using the app
        purpose_label = QLabel("What is your goal with CueYou?", self)
        purpose_label.setFont(QFont("Source Sans Pro", 12))
        purpose_label.setStyleSheet("color: #1D263B")
        self.usage_purpose_dropdown = QComboBox(self)
        self.usage_purpose_dropdown.setStyleSheet(stylesheettext)
        self.usage_purpose_dropdown.addItems([
            'Select Purpose', 'Job interviews', 'College interviews', 'General preparation'
        ])
        # Create account button
        self.create_account_button = QPushButton('Create Account', self)
        self.create_account_button.setFont(QFont("Source Sans Pro", 12))
        self.create_account_button.setStyleSheet("padding: 8px; background-color: #FF9F1C; color: white; border-radius: 15px;")
        self.create_account_button.clicked.connect(self.handle_signup)
        # Error label at the bottom of the screen
        self.error_label = QLabel("", self)
        self.error_label.setFont(QFont("Source Sans Pro", 12))
        self.error_label.setStyleSheet("color: red;")  # Style the error message in red

        self.back_button = QPushButton("Back to Login")
        self.back_button.setFont(QFont("Source Sans Pro", 12))
        self.back_button.setStyleSheet("padding: 8px; background-color: #003C8A; color: white; border-radius: 15px;")
        self.back_button.clicked.connect(lambda: self.switch_page_callback(2)) # switch to login page
        # Adding elements to the form layout
        form_layout.addRow(email_label,self.email_input)
        form_layout.addRow(name_label,self.name_input)
        form_layout.addRow(country_label, self.country_dropdown)
        form_layout.addRow(fieldofwork_label,self.field_of_work_dropdown)
        form_layout.addRow(position_label,self.position_dropdown)
        form_layout.addRow(experience_label, self.experience_dropdown)
        form_layout.addRow(checkbox_layout)
        form_layout.addRow(purpose_label,self.usage_purpose_dropdown)
        form_layout.addRow(password_label,self.password_input)
        form_layout.addRow(reenterpassword_label,self.reenter_password_input)
        form_layout.addRow(self.create_account_button)
        form_layout.addRow(self.back_button)
        form_layout.addRow(self.error_label)


        # Adding form layout to the scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollBar:vertical {
                background: #f2f2f2;
                width: 12px;
                margin: 0px 3px 0px 3px;
            }

            QScrollBar::handle:vertical {
                background: #B2B2B2;
                min-height: 20px;
                border-radius: 6px;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        scroll_widget = QWidget()
        scroll_widget.setLayout(form_layout)
        scroll_area.setWidget(scroll_widget)

        layout.addWidget(signup_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    @pyqtSlot()
    def handle_signup(self):
        email = self.email_input.text()
        name = self.name_input.text()
        password = self.password_input.text()
        reentered_password = self.reenter_password_input.text()
        country = self.country_dropdown.currentText()
        field_of_work = self.field_of_work_dropdown.currentText()
        position = self.position_dropdown.currentText()
        experience = self.experience_dropdown.currentText()
        is_student = self.student_checkbox.isChecked()
        usage_purpose = self.usage_purpose_dropdown.currentText()

        try:
            if password == reentered_password:
                if not self.validate_password(password):
                    self.error_label.setText("Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
                if self.validate_password(password):
                    result = add_user(name, email, password, country, field_of_work, position,
                        experience, is_student, usage_purpose)
                    if result == "Account created successfully":
                        self.switch_page_callback(2)  # Switch to login page
                    else:
                        # Display error message
                        self.error_label.setText(result)
            else:
                # Display error message
                print("Passwords do not match")
        except Exception as e:
            self.error_label.setText(f"Error occured; {e}")
            