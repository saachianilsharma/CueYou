from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from database import get_user_by_token, clear_session_token
import os
import sys


if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

class ProfilePage(QWidget):
    def __init__(self, switch_page_callback,get_user_details_callback):
        super().__init__()
        self.get_user_details_callback = get_user_details_callback
        self.username = ""
        self.user = None
        self.switch_page_callback = switch_page_callback
        self.init_ui()

    def update_profile(self):
        """Update the profile page with the user's information."""
        user_data = self.get_user_details_callback()
        print("user data in profile page",user_data)
        if user_data:
            self.profile_label.setText(user_data.get("name", "Jane Doe"))
            self.email_label.setText(user_data.get('emailid', 'N/A'))
            self.country_label.setText(user_data.get('country', 'N/A'))
            self.field_of_work_label.setText(user_data.get('field_of_work', 'N/A'))
            self.position_label.setText(user_data.get('position', 'N/A'))
            self.experience_label.setText(user_data.get('experience', 'N/A'))
            self.is_student_label.setText('Yes' if user_data.get('is_student') else 'No')
        else:
            self.error_label.setText("Error occurred in loading user data.")


    def logout(self):
        sessionfilepath = "session_token.txt"
        with open(sessionfilepath, 'r') as file:
            # Read the entire content of the file
            self.sessiontoken = file.read()
        clear_session_token(self.sessiontoken)
        with open(sessionfilepath, 'w') as file:
            pass
        self.switch_page_callback(2) # switch to login page
    
    def showEvent(self, event):
        super().showEvent(event)
        self.update_profile()  # Call update_profile when the page is shown

    def init_ui(self):
        # Fetch user by token
        #user = get_user_by_token(self.sessiontoken)
        # Main layout created
        main_layout = QVBoxLayout()
        self.setFont(QFont("Source Sans Pro", 12))
        
        # Profile illustration
        illustrationpath = os.path.join(base_path, 'images', 'profilehead.png')
        illustration_label = QLabel(self)
        illustration_pixmap = QPixmap(illustrationpath)  # Adjust path as needed
        illustration_label.setPixmap(illustration_pixmap)
        illustration_label.setScaledContents(True)
        illustration_label.setFixedSize(100,100)
        illustration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(illustration_label, alignment=Qt.AlignmentFlag.AlignCenter)
        # Error Label
        self.error_label = QLabel('', self)
        self.error_label.setStyleSheet("color: red;")
        #main_layout.addWidget(self.error_label)
        # Fetch user details
        
        # Profile Label
        self.profile_label = QLabel("Loading your Profile...")
        self.profile_label.setFont(QFont("Source Sans Pro", 18))
        self.profile_label.setStyleSheet("color: #1D263B; font-weight: bold;")
        self.profile_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.profile_label, alignment=Qt.AlignmentFlag.AlignCenter)
        #creating middle area
         # Adding elements to the form layout
        form_layout = QFormLayout() #QHBoxLayout()
        #display labels
        #left_layout = QVBoxLayout()
        self.email_label_display = QLabel("Email")
        self.email_label_display.setFont(QFont("Source Sans Pro", 12))
        self.email_label_display.setStyleSheet("color: #1D263B; font-weight: bold;")
        self.country_label_display = QLabel("Country")
        self.country_label_display.setFont(QFont("Source Sans Pro", 12))
        self.country_label_display.setStyleSheet("color: #1D263B; font-weight: bold;")
        self.field_of_work_label_display = QLabel("Field of Work")
        self.field_of_work_label_display.setFont(QFont("Source Sans Pro", 12))
        self.field_of_work_label_display.setStyleSheet("color: #1D263B; font-weight: bold;")
        self.position_label_display = QLabel("Position")
        self.position_label_display.setFont(QFont("Source Sans Pro", 12))
        self.position_label_display.setStyleSheet("color: #1D263B; font-weight: bold;")
        self.experience_label_display = QLabel("Experience")
        self.experience_label_display.setFont(QFont("Source Sans Pro", 12))
        self.experience_label_display.setStyleSheet("color: #1D263B;font-weight: bold;")
        self.is_student_label_display = QLabel("Student")
        self.is_student_label_display.setFont(QFont("Source Sans Pro", 12))
        self.is_student_label_display.setStyleSheet("color: #1D263B;font-weight: bold;")
        #value labels
        #right_layout = QVBoxLayout()
        self.email_label = QLabel("Loading...")
        self.email_label.setFont(QFont("Source Sans Pro", 12))
        self.email_label.setStyleSheet("color: #1D263B; margin-left: 20px;")
        self.country_label = QLabel("Loading...")
        self.country_label.setFont(QFont("Source Sans Pro", 12))
        self.country_label.setStyleSheet("color: #1D263B;margin-left: 20px;")
        self.field_of_work_label = QLabel("Loading...")
        self.field_of_work_label.setFont(QFont("Source Sans Pro", 12))
        self.field_of_work_label.setStyleSheet("color: #1D263B;margin-left: 20px;")
        self.position_label = QLabel("Loading...")
        self.position_label.setStyleSheet("color: #1D263B;margin-left: 20px;")
        self.position_label.setFont(QFont("Source Sans Pro", 12))
        self.experience_label = QLabel("Loading...")
        self.experience_label.setFont(QFont("Source Sans Pro", 12))
        self.experience_label.setStyleSheet("color: #1D263B;margin-left: 20px;")
        self.is_student_label = QLabel("Loading...")
        self.is_student_label.setFont(QFont("Source Sans Pro", 12))
        self.is_student_label.setStyleSheet("color: #1D263B;margin-left: 20px;")
        #main_layout.addWidget(self.name_label)

        #add layouts to main layout
         # Adding elements to the form layout
        form_layout.addRow(self.email_label_display,self.email_label)
        form_layout.addRow(self.country_label_display,self.country_label)
        form_layout.addRow(self.field_of_work_label_display,self.field_of_work_label)
        form_layout.addRow(self.position_label_display,self.position_label)
        form_layout.addRow(self.experience_label_display,self.experience_label)
        form_layout.addRow(self.is_student_label_display,self.is_student_label)
        """ middle_area.addLayout(left_layout)
        middle_area.addLayout(right_layout) """
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.error_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        # Create Back and Logout buttons
        # Back button
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
        self.back_button.clicked.connect(lambda: self.switch_page_callback(0)) # switch to home page
        main_layout.addWidget(self.back_button)
        # Log out button
        self.logout_button = QPushButton("Log Out")
        self.logout_button.setFont(QFont("Source Sans Pro", 12))
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9F1C;
                color: white;
                border-radius: 15px;
                padding: 5px 20px;
                font-size: 16px;
                
            }
            
        """)
        self.logout_button.clicked.connect(lambda: self.logout()) # switch to login page
        main_layout.addWidget(self.logout_button)
        self.setLayout(main_layout)
        #self.update_profile()
     
