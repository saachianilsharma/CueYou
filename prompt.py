from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication
from PyQt6.QtGui import QFont, QPalette, QColor

class PromptWidget(QWidget):
    def __init__(self, message='', parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.ToolTip)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        self.label = QLabel(message)
        self.label.setStyleSheet("""color: black; font-family: 'Source Sans Pro'; font-size: 20px; padding: 10px; background-color: rgba(178, 178, 178, 150); border-radius: 15px;""")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        # Set the size and position of the widget
        self.resize(300, 50)
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2 #screen_geometry.width() - self.width() - 20
        y = screen_geometry.height() - self.height() - 60 #screen_geometry.height() - self.height() - 60
        self.move(x, y)

        # Timer to close the notification after 4 seconds
        #
        QTimer.singleShot(4000, self.close)
        """ self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close)
        self.timer.start(4000) """
        
    def set_message(self, message):
        self.label.setText(message)
