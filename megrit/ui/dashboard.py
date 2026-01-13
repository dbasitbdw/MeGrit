from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QStackedWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal

from megrit.components.navbar import Navbar
from megrit.components.logout import Logout
from megrit.components.header import HeaderWidget
from megrit.components.input import SearchInput
from megrit.components.category import CategoryCard
from megrit.components.priority import PriorityCard
from megrit.components.task_table import TaskTable, StreakWidget, ProgressBarWidget

from megrit.ui.pomodoro import PomodoroPage
from megrit.ui.add_task import AddTaskPage

from megrit.logic.task_manager import TaskManager
from megrit.logic.search_filter import SearchFilter
from megrit.logic.priority_manager import PriorityManager


class Home(QWidget):

    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("background-color: #fef8e9;")
        
        self.content_layout = QVBoxLayout(self)
        self.content_layout.setContentsMargins(15, 12, 15, 12)
        self.content_layout.setSpacing(10)
        self.content_layout.setAlignment(Qt.AlignTop)
   
        self.hello_label = HeaderWidget("Meisya")
        self.content_layout.addWidget(self.hello_label)
        
        self.search_layout = QHBoxLayout()
        self.search_layout.setSpacing(8)
        
        self.search_input = SearchInput()
        self.search_layout.addWidget(self.search_input)
        
        self.search_btn = QPushButton("SEARCH")
        self.search_btn.setFixedSize(90, 38)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(154, 177, 207);
                border: 2px solid rgba(0, 0, 0, 0.25);
                color: #000000;
                border-radius: 10px;
                font-family: 'Dreaming Outloud AllCaps';
                font-weight: bold;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: rgb(134, 157, 187);
            }
        """)
        self.search_btn.clicked.connect(self.on_search_clicked)
        self.search_layout.addWidget(self.search_btn)
        
        self.entry_btn = QPushButton("NEW ENTRY")
        self.entry_btn.setFixedSize(110, 38)
        self.entry_btn.setStyleSheet("""
            QPushButton {
                background-color: #e8a8a6;
                border: 2px solid rgba(0, 0, 0, 0.25);
                color: #000000;
                border-radius: 10px;
                font-family: 'Dreaming Outloud AllCaps';
                font-weight: bold;
                font-size: 22px;
            }
            QPushButton:hover {
                background-color: #d89896;
            }
        """)
        self.entry_btn.clicked.connect(self.on_new_entry_clicked)
        self.search_layout.addWidget(self.entry_btn)
        
        self.content_layout.addLayout(self.search_layout)
        
        self.status_layout = QHBoxLayout()
        self.status_layout.setSpacing(12)
        
        today_count = self.task_manager.count_today_entries()
        self.card_entry = CategoryCard(count=today_count)
        self.status_layout.addWidget(self.card_entry)
        
        high_priority_count = PriorityManager.count_high_priority(self.task_manager.get_all_tasks())
        self.card_priority = PriorityCard(count=high_priority_count)
        self.status_layout.addWidget(self.card_priority)
        
        self.content_layout.addLayout(self.status_layout)
        
        self.table = TaskTable()
        self.table.task_status_changed.connect(self.on_task_status_changed)
        self.table.task_deleted.connect(self.on_task_deleted)
        
        self.content_layout.addWidget(self.table)
        
        self.bottom_wrapper = QWidget()
        self.bottom_layout = QVBoxLayout(self.bottom_wrapper)
        self.bottom_layout.setContentsMargins(0, 5, 0, 0)
        self.bottom_layout.setSpacing(5)
        
        self.streak_entry = StreakWidget()
        self.bottom_layout.addWidget(self.streak_entry, alignment=Qt.AlignCenter)
        
        self.pbar = ProgressBarWidget()
        self.bottom_layout.addWidget(self.pbar, alignment=Qt.AlignCenter)
        
        self.content_layout.addWidget(self.bottom_wrapper)
        
        self.content_layout.addSpacerItem(
            QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
    
    def on_search_clicked(self):
        query = self.search_input.text()
        if query:
            filtered_tasks = SearchFilter.filter_by_description(
                self.task_manager.get_all_tasks(), 
                query
            )
            print(f"Searching for: {query}")
            print(f"Found {len(filtered_tasks)} tasks")
            
            if not filtered_tasks:
                from PyQt5.QtWidgets import QMessageBox
                msg = QMessageBox(self)
                msg.setWindowTitle("Search Result")
                msg.setText("What you are looking for was not found")
                msg.setIcon(QMessageBox.Information)
                msg.setStyleSheet("""
                    QMessageBox { background-color: #fffaf0; } 
                    QMessageBox QLabel { color: black; }
                    QPushButton {
                        background-color: #e8a8a6;
                        color: black;
                        border: 1px solid gray;
                        border-radius: 5px;
                        padding: 5px 15px;
                        font-family: 'Poppins';
                    }
                    QPushButton:hover {
                        background-color: #d89896;
                    }
                """)
                msg.exec_()
                self.table.load_tasks([]) 
            else:
                self.table.load_tasks(filtered_tasks)
        else:
            self.refresh_data()
    
    def on_new_entry_clicked(self):
        parent = self.window()
        if hasattr(parent, 'dashboard'):
            pass
    
    def refresh_counts(self):
        today_count = self.task_manager.count_today_entries()
        self.card_entry.update_count(today_count)
        
        high_priority_count = PriorityManager.count_high_priority(
            self.task_manager.get_all_tasks()
        )
        self.card_priority.update_count(high_priority_count)
     
        streak_count = self.task_manager.calculate_streak()
        self.streak_entry.update_streak(streak_count)
        self.pbar.update_progress(streak_count)

    def on_task_status_changed(self, task_id, is_completed):
        self.task_manager.update_task_status(task_id, is_completed)
        self.refresh_data()

    def on_task_deleted(self, task_id):
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle("Hapus Task")
        msg.setText("Apakah anda yakin ingin menghapus task ini?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        msg.setStyleSheet("QMessageBox { background-color: #fffaf0; } QMessageBox QLabel { color: black; }")
        
        yes_btn = msg.button(QMessageBox.Yes)
        yes_btn.setText("Yes")
        yes_btn.setStyleSheet("""
            QPushButton {
                background-color: #e8a8a6;
                color: black; 
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px 15px;
                font-family: 'Poppins';
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d89896;
            }
        """)
        
        no_btn = msg.button(QMessageBox.No)
        no_btn.setText("No")
        no_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px 15px;
                font-family: 'Poppins';
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        
        if msg.exec_() == QMessageBox.Yes:
            self.task_manager.delete_task(task_id)
            self.refresh_data()
    
    def set_username(self, username):
     
        self.hello_label.set_username(username)
        self.task_manager.set_user(username)
        self.refresh_data()

    def refresh_data(self):
 
        self.refresh_counts()
        self.table.load_tasks(self.task_manager.get_all_tasks())


class Dashboard(QWidget):

    logout_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fef8e9;")
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.navbar = Navbar(self)
        layout.addWidget(self.navbar, 0, Qt.AlignTop)

        self.main_content = QStackedWidget()
    
        self.home_page = Home()
        self.main_content.addWidget(self.home_page)
    
        self.pomodoro_page = PomodoroPage()
        self.main_content.addWidget(self.pomodoro_page) 
        
        self.add_task_page = AddTaskPage(self.home_page.task_manager)
        self.main_content.addWidget(self.add_task_page) 
        
        layout.addWidget(self.main_content, 1)
        self.setLayout(layout)
    
        self.navbar.btn_home.clicked.connect(lambda: self.main_content.setCurrentIndex(0))
        self.navbar.btn_tasks.clicked.connect(lambda: self.main_content.setCurrentIndex(1))
        self.navbar.btn_logout.clicked.connect(self.confirm_logout)

        self.home_page.entry_btn.clicked.connect(lambda: self.main_content.setCurrentIndex(2))
        
        self.add_task_page.task_added.connect(self.on_task_added)
        self.add_task_page.cancelled.connect(lambda: self.main_content.setCurrentIndex(0))

    def on_task_added(self):

        self.home_page.refresh_counts()
        self.home_page.refresh_data()
        self.main_content.setCurrentIndex(0)

    def confirm_logout(self):
        if Logout.confirm(self):
            self.logout_signal.emit()
    
    def set_username(self, username):
      
        self.home_page.set_username(username)
