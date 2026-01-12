from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

class CategoryCard(QFrame):
    
    def __init__(self, count=0, parent=None):
        super().__init__(parent)
        self.count = count
        self.setup_ui()
        self.update_count(self.count)
    
    def setup_ui(self):
        self.setFixedHeight(48)
        self.setStyleSheet("""
            QFrame{
                background-color:rgba(177, 200, 239, 0.25);
                border: 2px solid rgba(0,0,0,0.25);
                border-radius: 15px;
            }
            """)
        
        self.card_entry_layout = QHBoxLayout(self)
     
        self.entry_icon = QLabel(self)
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon", "task.png")
        pixmap_task = QPixmap(icon_path)
        scaled_pixmap_task = pixmap_task.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.entry_icon.setPixmap(scaled_pixmap_task)
        self.entry_icon.setFixedSize(32, 32)
        self.entry_icon.move(10, 8)
        self.entry_icon.setStyleSheet("background: transparent; border: none;")
 
        self.card_entry_labelA = QLabel("Today's Entries")
        self.card_entry_labelA.setStyleSheet("""
            QLabel {
                font-size: 16px; 
                font-family: 'Poppins';
                font-weight: bold;
                color: #000000;
                padding-left: 60px;  
                border: none;
                background: transparent;
            }
        """)

        self.count_label = QLabel(str(self.count))
        self.count_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-family: 'Poppins';
                font-weight: bold;
                color: #000000;
                padding-right: 20px;
                border: none;
                background: transparent;
            }
        """)
        
        self.card_entry_layout.addWidget(self.card_entry_labelA)
        self.card_entry_layout.addStretch()
        self.card_entry_layout.addWidget(self.count_label)
    
    def update_count(self, count):
        self.count = count
        self.count_label.setText(str(count))

