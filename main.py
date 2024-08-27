import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon
from login import LoginPage
from signup import SignupPage
from forgotpassword import ForgotPasswordPage
from cuesessionpage import CueSessionPage
from splash import SplashScreen
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #self.setWindowTitle('CueYou')
        self.setStyleSheet("background-color: white;")
        #self.setGeometry(100, 100, 400, 200)
        self.setFixedSize(720, 390)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login_page = LoginPage(self.switch_page)
        self.signup_page = SignupPage(self.switch_page)
        self.forgot_password_page = ForgotPasswordPage(self.switch_page)
        #self.profile_page = ProfilePage(self.switch_page)
        self.cue_session_page = CueSessionPage()

        #self.central_widget.addWidget(self.login_page) #index 0
        self.central_widget.addWidget(self.cue_session_page) #index 1
        #self.central_widget.addWidget(self.signup_page) #index 2
        #self.central_widget.addWidget(self.forgot_password_page) #index 3

    def switch_page(self, page_index):
        self.central_widget.setCurrentIndex(page_index)

def main():
    app = QApplication(sys.argv)
    # Set the application icon
    app.setWindowIcon(QIcon("images/logoicon.ico"))

    # Create and display the splash screen
    splash = SplashScreen()
    splash.display(3000)  # Display for 3 seconds
    main_window = MainWindow()
    main_window.setWindowTitle("CueYou - Executive Presence Coach")
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
