from PyQt5.QtWidgets import QApplication, QStackedWidget, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from megrit.ui.splash import SplashScreen
from megrit.ui.login import LoginScreen
from megrit.ui.dashboard import Dashboard

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MeGrit")
        self.setStyleSheet("background-color: #fef8e9;") 
        
        self.setFixedSize(800, 650)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        self.splash = SplashScreen()
        self.login = LoginScreen()
        self.dashboard = None 
        self.dashboard = Dashboard()

        self.stack.addWidget(self.splash) 
        self.stack.addWidget(self.login) 
        self.stack.addWidget(self.dashboard) 
        self.splash.finished.connect(self.show_login)
        self.login.login_success.connect(self.show_dashboard)
        self.dashboard.logout_signal.connect(self.handle_logout)
        
        self.stack.setCurrentIndex(0)

    def show_login(self):
        self.stack.setCurrentIndex(1)
        self.setFixedSize(800, 650) 

    def show_dashboard(self, username):
        print(f"User logged in: {username}")
        self.dashboard.set_username(username)
        self.setFixedSize(800, 650)
        self.stack.setCurrentIndex(2)

    def handle_logout(self):
        self.stack.setCurrentIndex(0)
        self.setFixedSize(800, 650)
        self.login.username_input.clear() 
        self.stack.removeWidget(self.splash)
        self.splash = SplashScreen()
        self.splash.finished.connect(self.show_login)
        self.stack.insertWidget(0, self.splash)
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
