from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal
import os

class SplashScreen(QWidget):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.bg = QLabel(self)
        
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        splash_path = os.path.join(base_path, "assets", "image", "splash.png")
        
        self.bg.setPixmap(QPixmap(splash_path))
        self.bg.setScaledContents(True)
        self.bg.resize(800, 450) 

        QTimer.singleShot(3000, self.finish)

    def finish(self):
        self.finished.emit()
    
    def resizeEvent(self, event):
        self.bg.resize(self.size())
        super().resizeEvent(event)
