from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDial, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTime

class TimePickerDialog(QDialog):
    def __init__(self, parent=None, initial_time=None):
        super().__init__(parent)
        self.setWindowTitle("Select Time")
        self.setFixedSize(300, 350)
        self.setStyleSheet("background-color: #fffaf0; color: black;")
        
        self.selected_time = initial_time if initial_time else QTime.currentTime()
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        self.display_label = QLabel(self.selected_time.toString("HH:mm"))
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            font-family: 'Dreaming Outloud AllCaps', 'Poppins', sans-serif;
            color: #333;
            background: transparent;
        """)
        layout.addWidget(self.display_label)
        
        dial_layout = QHBoxLayout()
        
        self.hour_dial = QDial()
        self.hour_dial.setMinimum(0)
        self.hour_dial.setMaximum(23)
        self.hour_dial.setValue(self.selected_time.hour())
        self.hour_dial.setNotchesVisible(True)
        self.hour_dial.setFixedSize(100, 100)
        self.hour_dial.valueChanged.connect(self.update_time_from_dials)
        self.hour_dial.setStyleSheet("background-color: #eee; border-radius: 50px;")
        
        self.minute_dial = QDial()
        self.minute_dial.setMinimum(0)
        self.minute_dial.setMaximum(59)
        self.minute_dial.setValue(self.selected_time.minute())
        self.minute_dial.setNotchesVisible(True)
        self.minute_dial.setFixedSize(100, 100)
        self.minute_dial.valueChanged.connect(self.update_time_from_dials)
        self.minute_dial.setStyleSheet("background-color: #eee; border-radius: 50px;")
        
        dial_layout.addWidget(self.hour_dial)
        dial_layout.addWidget(self.minute_dial)
        layout.addLayout(dial_layout)
        
        labels_layout = QHBoxLayout()
        l1 = QLabel("HOURS")
        l1.setAlignment(Qt.AlignCenter)
        l2 = QLabel("MINS")
        l2.setAlignment(Qt.AlignCenter)
        labels_layout.addWidget(l1)
        labels_layout.addWidget(l2)
        layout.addLayout(labels_layout)
        
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("SET TIME")
        ok_btn.clicked.connect(self.accept)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        
        cancel_btn = QPushButton("CANCEL")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #d32f2f; }
        """)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)

    def update_time_from_dials(self):
        h = self.hour_dial.value()
        m = self.minute_dial.value()
        self.selected_time = QTime(h, m)
        self.display_label.setText(self.selected_time.toString("HH:mm"))

    def get_time(self):
        return self.selected_time
