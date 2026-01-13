from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
import os
import json

class LoginScreen(QWidget):
    login_success = pyqtSignal(str)

    def __init__(self):
        super().__init__()
    
        self.bg = QLabel(self)
        
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        login_path = os.path.join(base_path, "assets", "image", "login.png")
        
        self.bg.setPixmap(QPixmap(login_path))
        self.bg.setScaledContents(True)
        self.bg.resize(800, 650) 

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("enter here")
        self.username_input.setGeometry(200, 420, 300, 40) 
        self.load_saved_user()
        self.username_input.setStyleSheet("""
            QLineEdit {
                border-radius: 20px;
                padding-left: 15px;
                background-color: #dddddd;
                font-size: 14px;
                color: black;
            }
        """)
        self.username_input.returnPressed.connect(self.attempt_login)

        self.enter_btn = QPushButton("Enter", self)
        self.username_input.setGeometry(200, 420, 320, 40)
        self.enter_btn.setGeometry(530, 420, 80, 40)
        self.enter_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: black;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.enter_btn.clicked.connect(self.attempt_login)

    def attempt_login(self):
        username = self.username_input.text().strip()
        if not username:
            msg = QMessageBox(self)
            msg.setWindowTitle("Validation Error")
            msg.setText("Please enter a username.")
            msg.setIcon(QMessageBox.Warning)
            msg.setIcon(QMessageBox.Warning)
            
            ok_btn = msg.addButton("OK", QMessageBox.AcceptRole)
            
            msg.setStyleSheet("""
                QMessageBox { background-color: white; color: black; }
                QLabel { color: black; font-size: 14px; }
                QPushButton { 
                    color: black !important;
                    background-color: #e0e0e0;
                    border: 1px solid #999999; 
                    border-radius: 4px;
                    padding: 6px 15px; 
                    font-weight: bold;
                    min-width: 60px;
                }
                QPushButton:hover { background-color: #d0d0d0; }
            """)
            ok_btn.setStyleSheet("""
                QPushButton { 
                    color: black !important; 
                    background-color: #e0e0e0; 
                    border: 1px solid #999999;
                    padding: 5px 15px;
                    min-width: 60px;
                } 
                QPushButton:hover { background-color: #c0c0c0; }
            """)
                
            msg.exec_()
            return

        self.save_user(username)
        self.login_success.emit(username)

    def save_user(self, username):
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_path, "data")
            os.makedirs(data_dir, exist_ok=True)
            
            users_file = os.path.join(data_dir, "users.json")
            users = []
            if os.path.exists(users_file):
                try:
                    with open(users_file, 'r') as f:
                        users = json.load(f)
                        if not isinstance(users, list):
                            users = []
                except:
                    users = []
            
            if username not in users:
                users.append(username)
                with open(users_file, 'w') as f:
                    json.dump(users, f, indent=4)
        except Exception as e:
            print(f"Error saving user: {e}")

    def load_saved_user(self):
        pass

    def resizeEvent(self, event):
        self.bg.resize(self.size())
        super().resizeEvent(event)
