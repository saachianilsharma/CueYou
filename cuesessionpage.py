from PyQt6.QtWidgets import QWidget, QHBoxLayout,QVBoxLayout, QPushButton, QLabel, QComboBox, QComboBox, QGridLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from audiomonitor import AudioMonitorPage
from videomonitor import VideoMonitorPage
from prompt import PromptWidget
import os
import sys
from database import get_user_by_token

class CueSessionPage(QWidget):
    def __init__(self,switch_page_callback,get_user_data_callback):
        super().__init__()
        
        self.get_user_data_callback = get_user_data_callback
        self.username = "Profile"
        self.switch_page_callback = switch_page_callback
        self.prompt = PromptWidget() #single object to be passed as reference to audio and video classes
        self.audio_monitor = AudioMonitorPage(prompt_widget=self.prompt)
        self.video_monitor = VideoMonitorPage(prompt_widget=self.prompt)
        self.initUI()
    def initUI(self):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        # Fetching user data using callback
        """ user_data = self.get_user_data_callback()
        if user_data:
            self.username = user_data.get("name", "JaneDoe")
        else:
            self.username = "JaneDoe"
            print("Could not fetch user data") """

        # Accessing an individual image
        illustrationpath = os.path.join(base_path, 'images', 'homepageillustration25-modified-small.png')
        logopath = os.path.join(base_path, 'images', 'homepagelogo.png')
        arrowpath = os.path.join(base_path, 'images', 'white-arrow.png').replace("\\", "/")
        #Main Layout
        main_layout = QGridLayout()
        #main_layout.setContentsMargins(10, 10, 10, 0)
        main_layout.setHorizontalSpacing(20)
        main_layout.setVerticalSpacing(0)
        #Left side layout for illustration
        
        illustration_label = QLabel(self)
        illustration_pixmap = QPixmap(illustrationpath)  # Adjust path as needed
        illustration_label.setPixmap(illustration_pixmap)
        illustration_label.setScaledContents(True)
        illustration_label.setFixedSize(329, 365)
        
        #illustration_label.setFixedSize(illustration_pixmap.size())
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(logopath)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(184, 82)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Welcome label
        welcome_label = QLabel("Welcome to CueYou!")
        welcome_label.setFont(QFont('Source Sans Pro', 24))
        welcome_label.setStyleSheet("color: #1D263B; padding: 5px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Subtitle label
        """ subtitle_label = QLabel("Ready to ace your next interview?")
        subtitle_label.setFont(QFont('Arial', 14))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(subtitle_label) """

        # Buttons layout
        self.start_button = QPushButton("Start Cue Session")
        self.start_button.clicked.connect(self.start_cue_session)
        self.start_button.setStyleSheet("""
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

        self.end_button = QPushButton("End Cue Session")
        self.end_button.clicked.connect(self.end_cue_session)
        self.end_button.setStyleSheet("""
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
        self.end_button.setDisabled(True)

        #profile page button
        
        self.profile = QPushButton(self.username) 
        self.profile.clicked.connect(lambda: self.switch_page_callback(1)) # switch to profile page
        self.profile.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1D263B;
                border-radius: 15px;
                padding: 5px 20px;
                font-size: 15px;
                border: 1px solid #1D263B;
            }
        """)
       

        self.dropdown = QComboBox()
        self.dropdown.addItems(["Audio", "Video", "Both"])
        self.dropdown.setFixedHeight(self.start_button.sizeHint().height())
        #self.dropdown.setStyleSheet("background-color: #1D263B;border-radius: 15px; color: white;padding: 10px 20px; font-size: 16px;")
        stylesheettext="""
            QComboBox {
                
                border-radius: 15px;
                padding: 5px 20px;
                font-size: 14px;
                background-color: #1D263B;
                color: white;
                
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
                color: white;
                background-color: #1D263B;
            }
            QComboBox::down-arrow {
                width: 10px;
                image: url("""+str(arrowpath)+""");
                height: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #1D263B;  /* Background color of dropdown items */
                color: white;  /* Text color of dropdown items */
                selection-background-color: #003C8A;  /* Background color for selected item */
                selection-color: white;  /* Text color for selected item */
            }
        """
        #print(stylesheettext)
        self.dropdown.setStyleSheet(stylesheettext)
        

        
        # Layout for buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.end_button)
        button_layout.addSpacing(10)
        #button_layout.addWidget(self.dropdown)


        # Adding widgets to main layout
        main_layout.addWidget(illustration_label, 0, 0, 5, 1, Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(self.profile, 0, 1, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(logo_label, 1, 1, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(welcome_label, 2, 1, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(button_layout, 3, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.dropdown, 4, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        #main_layout.setRowStretch(1, 0)
        main_layout.setColumnStretch(2,0)
        main_layout.setRowStretch(0, 0)  # For the illustration row
        main_layout.setRowStretch(1, 0)  # For the welcome label row
        main_layout.setRowStretch(2, 1)  # For the buttons row
        main_layout.setRowStretch(3, 0)  # For the dropdown row
        main_layout.setRowStretch(4, 1)  # Add space below if needed
        self.setLayout(main_layout)
        #self.setFixedSize(self.sizeHint())
        #self.setFixedSize(710, 400)
        self.update_user_data()  # Load user data when initializing UI
    
    def update_user_data(self):
        """Update UI elements with the user's information."""
        user_data = self.get_user_data_callback()
        print("update_user_data called , user = ", user_data)
        if user_data:
            self.username = user_data.get('name', 'JaneDoe')
            
            #self.username_label.setText(f"Welcome, {username}!")
            #self.profile_button.setText(f"Profile: {username}")
        else:
            self.profile.setText("JaneDoe")
            print("No user data available to update CueSessionPage.")
        self.profile.setText(self.username.split(' ', 1)[0])


    def display_prompt(self, message):
        #self.prompt_label.setText(message)
        prompt = PromptWidget(message)
        prompt.show()


    def start_cue_session(self):
        mode = self.dropdown.currentText()
        if mode == "Audio":
            self.audio_monitor.start()
        elif mode == "Video":
            self.video_monitor.start()
        elif mode == "Both":
            self.audio_monitor.start()
            self.video_monitor.start()

        self.start_button.setDisabled(True)
        self.end_button.setDisabled(False)
        self.dropdown.setDisabled(True)

    def end_cue_session(self):
        mode = self.dropdown.currentText()
        if mode == "Audio":
            self.audio_monitor.stop()
        elif mode == "Video":
            self.video_monitor.stop()
        elif mode == "Both":
            self.audio_monitor.stop()
            self.video_monitor.stop()
        self.start_button.setDisabled(False)
        self.end_button.setDisabled(True)
        self.dropdown.setDisabled(False)
        self.display_prompt("Cue Session Ended successfully.")
