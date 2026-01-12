from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import pyqtSignal

class TaskCheckbox(QCheckBox):
    
    status_changed = pyqtSignal(bool) 
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.stateChanged.connect(self.on_state_changed)
    
    def setup_ui(self):
        self.setStyleSheet("""
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid rgba(0, 0, 0, 0.25);
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #9AB3D5;
                border: 2px solid #9AB3D5;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #9AB3D5;
            }
        """)
    
    def on_state_changed(self, state):
        self.status_changed.emit(self.isChecked())
