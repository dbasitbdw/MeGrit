from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
import os

class Navbar(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setAttribute(Qt.WA_StyledBackground, True) 
		self.setObjectName("Navbar") 
		self.init_ui()
		self.setStyleSheet(self.qss())


	def init_ui(self):
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(0, 10, 0, 10)
		self.layout.setSpacing(30)
		self.layout.setAlignment(Qt.AlignTop)

		self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon")

		self.btn_menu = QPushButton()
		self.btn_menu.setIcon(QIcon(os.path.join(self.icon_path, "close.png")))
		self.btn_menu.setIconSize(QSize(36, 36))
		self.btn_menu.setObjectName("MenuButton")
		self.btn_menu.setCursor(Qt.PointingHandCursor)
		self.btn_menu.clicked.connect(self.toggle_menu)
		self.layout.addWidget(self.btn_menu)

		self.separator = QFrame()
		self.separator.setFrameShape(QFrame.HLine)
		self.separator.setFrameShadow(QFrame.Plain)
		self.separator.setStyleSheet("background-color: #bfbcb4; min-height: 2px; max-height: 2px; border: none; margin: 0px 10px;") # Margin kiri-kanan agar rapi
		self.layout.addWidget(self.separator)

		self.btn_home = QPushButton()
		self.btn_home.setIcon(QIcon(os.path.join(self.icon_path, "home.png")))
		self.btn_home.setIconSize(QSize(36, 36))
		self.btn_home.setObjectName("HomeButton")
		self.btn_home.setCursor(Qt.PointingHandCursor)
		self.layout.addWidget(self.btn_home)

		self.btn_tasks = QPushButton()
		self.btn_tasks.setIcon(QIcon(os.path.join(self.icon_path, "pomodoro.png")))
		self.btn_tasks.setIconSize(QSize(36, 36))
		self.btn_tasks.setObjectName("PomodoroButton")
		self.btn_tasks.setCursor(Qt.PointingHandCursor)
		self.layout.addWidget(self.btn_tasks)

		self.btn_logout = QPushButton()
		self.btn_logout.setIcon(QIcon(os.path.join(self.icon_path, "logout.png")))
		self.btn_logout.setIconSize(QSize(36, 36))
		self.btn_logout.setObjectName("LogoutButton")
		self.btn_logout.setCursor(Qt.PointingHandCursor)
		self.layout.addWidget(self.btn_logout)

		self.setLayout(self.layout)
		self.is_expanded = True

	def toggle_menu(self):
		self.is_expanded = not self.is_expanded
		
		if self.is_expanded:
			self.btn_menu.setIcon(QIcon(os.path.join(self.icon_path, "close.png")))
			self.separator.show()
			self.btn_home.show()
			self.btn_tasks.show()
			self.btn_logout.show()
		else:
			self.btn_menu.setIcon(QIcon(os.path.join(self.icon_path, "menu.png")))
			self.separator.hide()
			self.btn_home.hide()
			self.btn_tasks.hide()
			self.btn_logout.hide()
			
		self.adjustSize()

	def qss(self):
		return """
		QWidget#Navbar {
			background: #fef8e9;
			border: 3px solid #bfbcb4;
			border-radius: 18px;
			min-width: 80px;
			max-width: 80px;
			margin: 10px;
		}
		QPushButton {
			background: transparent;
			border: none;
			padding: 8px;
            margin: 0px 10px; /* Shrink hover area horizontally */
		}
		QPushButton:hover {
			background: #E3DFD6;
			border-radius: 12px;
		}
		QPushButton:pressed {
			background: #D6D3C7;
		}
		"""