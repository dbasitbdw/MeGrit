from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase
import os

class HeaderWidget(QLabel):
    
    def __init__(self, username="User", parent=None):
        super().__init__(parent)
        self.username = username
        self.load_font()
        self.setup_ui()
    
    def load_font(self):
        font_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "assets", "font", "dreaming-outloud-allcaps-regular.otf"
        )
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            self.font_family = "Arial"  # Fallback
    
    def setup_ui(self):
        self.setText(f"Hello, {self.username}")
        self.setStyleSheet(f"""
            QLabel {{
                font-size: 22px;
                color: #000000;
                font-family: '{self.font_family}';
                font-weight: normal;
            }}
        """)
    
    def set_username(self, username):
        self.username = username
        self.setText(f"Hello, {self.username}")
