from PyQt6.QtWidgets import QSplashScreen, QApplication, QMainWindow
from PyQt6.QtGui import QPixmap
import time

class SplashScreen(QSplashScreen):
    def __init__(self):
        # Load the image for the splash screen
        pixmap = QPixmap("images/cuesplash.jpg")
        super().__init__(pixmap)

    def display(self, duration=3000):
        # Display the splash screen for the given duration (in milliseconds)
        self.show()
        time.sleep(duration / 1000)  # Sleep in seconds
        self.close()
