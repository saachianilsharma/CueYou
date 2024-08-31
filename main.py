import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon, QFont
from login import LoginPage
from signup import SignupPage
from forgotpassword import ForgotPasswordPage
from cuesessionpage import CueSessionPage
from profilepage import ProfilePage
from splash import SplashScreen
import os
import sys
from database import get_user_by_token  # Function to get user by session token from DB

class MainWindow(QMainWindow):
    def __init__(self,sessiontoken):
        super().__init__()
        self.sessiontokenvalue = sessiontoken
        self.user_data = None  # MODIFIED: Store user data to pass between pages
        self.profile_page = None
         # Check if there's a valid session at startup
        user = self.check_existing_session()
        print("Checking existing session in main init - ", user)
        if user:
            self.user_data = user
            print("Checking existing session in main init if user - ", self.user_data)
            #self.cue_session_page.update_user_data()
        self.initUI()
        
    
    def check_existing_session(self):
        # Attempt to read the session token, either from file or directly from the database
        try:
            # MODIFIED: Removed reading from file and directly checked session value from the argument
            print ("calling get_user_by_token from main.py")
            user = get_user_by_token(self.sessiontokenvalue)
            if user:
                self.user_data = user  # MODIFIED: Save user data if session is valid
                print("Valid session found. Redirecting to CueSessionPage.")
                return user  # Returns user data if the session is valid
            else:
                print("Session token invalid or expired. Redirecting to LoginPage.")
                return None
        except Exception as e:
            # Handle other exceptions
            print(f"Error checking session: {e}")
            return None

    def initUI(self):
        self.setFont(QFont("Source Sans Pro", 12))
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(720, 390)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login_page = LoginPage(self.switch_page, self.set_user_data)
        self.signup_page = SignupPage(self.switch_page)
        self.forgot_password_page = ForgotPasswordPage(self.switch_page)
        self.profile_page = ProfilePage(self.switch_page, self.get_user_data) # MODIFIED: Load data on access
        self.cue_session_page = CueSessionPage(self.switch_page, self.get_user_data) # MODIFIED: Pass get_user_data callback

        self.central_widget.addWidget(self.cue_session_page) #index 0
        self.central_widget.addWidget(self.profile_page) #index 1
        self.central_widget.addWidget(self.login_page) #index 2
        self.central_widget.addWidget(self.signup_page) #index 3
        self.central_widget.addWidget(self.forgot_password_page) #index 4
        
        # Direct user to the appropriate page based on session presence
        if self.user_data:
            # Redirect to CueSessionPage if session exists
            self.switch_page(0)  # Redirect to CueSessionPage
        else:
            # Redirect to LoginPage if no session exists
            self.switch_page(2)

    def switch_page(self, page_index):
        self.central_widget.setCurrentIndex(page_index)

    def set_user_data(self, user_data):
        """Callback to set user data after successful login"""
        self.user_data = user_data
        self.cue_session_page.update_user_data()  # MODIFIED: Pass data to CueSessionPage

    def get_user_data(self):
        """Returns the current user data"""
        return self.user_data
    

def main():

    app = QApplication(sys.argv)
    
    # Set the application icon
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    # Accessing an individual image
    logoiconpath = os.path.join(base_path, 'images', 'logoicon.ico')
    sessionfilepath = "session_token.txt"
    try:
        with open(sessionfilepath, 'r') as file:
            sessiontoken = file.read().strip()  # Strip whitespace/newlines
    except FileNotFoundError:
        print("Session token file not found. Proceeding to LoginPage.")
    except Exception as e:
        print(f"Error reading session token: {e}")
    app.setWindowIcon(QIcon(logoiconpath))
    # Create and display the splash screen
    splash = SplashScreen()
    splash.display(3000)  # Display for 3 seconds
    main_window = MainWindow(sessiontoken)
    main_window.setWindowTitle("CueYou - Executive Presence Coach")
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
