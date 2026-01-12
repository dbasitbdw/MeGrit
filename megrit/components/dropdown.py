from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal

class CategoryDropdown(QComboBox):
    
    category_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.currentTextChanged.connect(self.on_selection_changed)
    
    def setup_ui(self):
     
        self.addItems(["Work", "Personal", "Study", "Health", "Other"])
        
        self.setStyleSheet("""
            QComboBox {
                background-color: rgba(177, 200, 239, 0.25);
                border: 2px solid rgba(0, 0, 0, 0.25);
                border-radius: 10px;
                padding: 5px 10px;
                font-family: 'Poppins';
                font-size: 14px;
                min-width: 100px;
            }
            QComboBox:hover {
                border: 2px solid #9AB3D5;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid rgba(0, 0, 0, 0.25);
                border-radius: 5px;
                selection-background-color: #9AB3D5;
                font-family: 'Poppins';
            }
        """)
    
    def on_selection_changed(self, text):
        self.category_selected.emit(text)


class PriorityDropdown(QComboBox):
    
    priority_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.currentTextChanged.connect(self.on_selection_changed)
    
    def setup_ui(self):
        # Priority levels
        self.addItems(["Low", "Medium", "High"])
        
        self.setStyleSheet("""
            QComboBox {
                background-color: rgba(177, 200, 239, 0.25);
                border: 2px solid rgba(0, 0, 0, 0.25);
                border-radius: 10px;
                padding: 5px 10px;
                font-family: 'Poppins';
                font-size: 14px;
                min-width: 100px;
            }
            QComboBox:hover {
                border: 2px solid #9AB3D5;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid rgba(0, 0, 0, 0.25);
                border-radius: 5px;
                selection-background-color: #9AB3D5;
                font-family: 'Poppins';
            }
        """)
    
    def on_selection_changed(self, text):
        self.priority_selected.emit(text)
