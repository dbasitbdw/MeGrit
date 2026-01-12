from PyQt5.QtWidgets import QLineEdit, QLabel
from PyQt5.QtGui import QPixmap, QFontDatabase
from PyQt5.QtCore import Qt
import os

class SearchInput(QLineEdit):
    
    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.setPlaceholderText("Search by description")
        self.setFixedHeight(38)
        
        # Add search icon
        self.search_icon = QLabel(self)
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon", "search.png")
        pixmap = QPixmap(icon_path)
        scaled_pixmap = pixmap.scaled(22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.search_icon.setPixmap(scaled_pixmap)
        self.search_icon.move(12, 8)
        self.search_icon.setStyleSheet("background: transparent; border: none;")
        
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(247, 242, 179, 0.25);
                border: 2px solid rgba(0, 0, 0, 0.25);
                border-radius: 15px;
                padding-left: 45px;
                font-family: '{self.font_family}';
                font-size: 15px;
                color: #000000;
            }}
            QLineEdit::placeholder {{
                color: #666666;
            }}
        """)
