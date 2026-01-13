from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
    QCheckBox, QPushButton, QMenu, QAction
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal
import os

class TaskTable(QTableWidget):
  
    task_status_changed = pyqtSignal(int, bool)
    task_deleted = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def load_tasks(self, tasks):
        self.setRowCount(0)
        if not tasks:
            return
            
        sorted_tasks = sorted(tasks, key=lambda x: (x.get('status') == 'Completed', x.get('created_at', '')))
        
        self.setRowCount(len(sorted_tasks))
        for row, task in enumerate(sorted_tasks):
            task_id = task.get('id')
            is_completed = task.get('status') == 'Completed'
    
            def create_item(text, col_index):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignCenter)
          
                if col_index == 1:
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                    if is_completed:
                        font = item.font()
                        font.setStrikeOut(True)
                        item.setFont(font)
                else:
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                
                return item

            created_at = task.get('created_at')
            date_str = ""
            if isinstance(created_at, str):
                date_str = created_at[:10]
            elif hasattr(created_at, 'strftime'):
                date_str = created_at.strftime("%d/%m/%y %H:%M")
            
            if 'scheduled_date' in task and 'scheduled_time' in task:
                date_str = f"{task['scheduled_date']} {task['scheduled_time'].replace('.', ':')}"
            
            self.setItem(row, 0, create_item(date_str, 0))
            self.setItem(row, 1, create_item(task.get('description', ''), 1))
            self.setItem(row, 2, create_item(task.get('category', ''), 2))
            self.setItem(row, 3, create_item(task.get('priority', ''), 3))
            
            checkbox_widget = QWidget()
            checkbox_widget.setStyleSheet("background: transparent;")
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            
            cb = QCheckBox()
            cb.setStyleSheet("""
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    border: 2px solid black;
                    border-radius: 4px;
                    background: white;
                }
                QCheckBox::indicator:checked {
                    image: url("/home/db/Tugas/Project Python Kelompok 1/megrit/assets/icon/check.svg");
                }
            """)
            cb.setChecked(is_completed)
            cb.setProperty("task_id", task_id)
            cb.stateChanged.connect(lambda state, tid=task_id: self.on_checkbox_changed(state, tid))
            
            checkbox_layout.addWidget(cb)
            self.setCellWidget(row, 4, checkbox_widget)

            action_widget = QWidget()
            action_widget.setStyleSheet("background: transparent;")
            action_layout = QHBoxLayout(action_widget)
            action_layout.setAlignment(Qt.AlignCenter)
            action_layout.setContentsMargins(0, 0, 0, 0) 
            action_layout.setSpacing(0)

            btn_menu = QPushButton("⋮")
            btn_menu.setFixedSize(30, 30)
            btn_menu.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    font-size: 18px; 
                    font-weight: bold;
                    color: #555;
                    padding: 0px; /* Force 0 padding */
                    margin: 0px;  /* Force 0 margin */
                }
                QPushButton:hover {
                    color: #000;
                    background-color: rgba(0,0,0,0.1);
                    border-radius: 15px;
                }
                QPushButton:pressed {
                    background-color: rgba(0,0,0,0.2);
                    border-radius: 15px;
                }
                QPushButton::menu-indicator {
                    image: none;
                }
            """)
            
            menu = QMenu(self)
            delete_action = QAction("Hapus", self)
            delete_action.triggered.connect(lambda checked, tid=task_id: self.on_delete_task(tid))
            menu.addAction(delete_action)
            
            btn_menu.setMenu(menu)

            action_layout.addWidget(btn_menu)
            self.setCellWidget(row, 5, action_widget)
            
        self.resizeRowsToContents()
            
    def on_checkbox_changed(self, state, task_id):
        self.task_status_changed.emit(task_id, state == Qt.Checked)
        
    def on_delete_task(self, task_id):
        self.task_deleted.emit(task_id)

    def set_callback(self, callback):
        self.parent_dashboard_callback = callback
    
    def setup_ui(self):
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["Date & time", "Description", "Category", "Priority", "Status", "Act"])
        self.setWordWrap(True)

        self.setMinimumHeight(400) 
        
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        
        self.setColumnWidth(0, 100) 
        self.setColumnWidth(2, 100) 
        self.setColumnWidth(3, 100) 
        self.setColumnWidth(4, 60)  
        self.setColumnWidth(5, 50)  

        self.verticalHeader().setVisible(False) 
        self.setShowGrid(False)                
        self.setFrameShape(QFrame.NoFrame)     
        
        self.setStyleSheet("""
            QTableWidget {
                background-color:rgba(177, 200, 239, 0.25);
                border: 1px solid rgba(0,0,0,0.1);      
                border-radius: 15px;
                font-family: 'Poppins';
                gridline-color: transparent;
                color: #000000;
                color: #000000;
            }
            QLineEdit {
                color: black;
                background-color: white;
                border: 1px solid #ccc;
            }
            QHeaderView::section {
                background-color:rgba(177, 200, 239, 0.25);
                border: none;                  
                border-bottom: 2px solid rgba(0,0,0,0.25);
                border-right: none;
                padding: 0px;
                font-family: 'Poppins';
                font-weight: bold;
                color: #000000;
                height: 35px;
                text-align: center;
            }
            QHeaderView::section:first {
                border-top-left-radius: 13px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 13px;
            }
            QTableWidget::item {
                border-bottom: none; 
                padding: 5px;
                color: #000000;
            }
            QMenu {
                background-color: white;
                border: 1px solid #ccc;
                font-family: 'Poppins';
                color: black;
            }
            QMenu::item {
                padding: 5px 20px;
                color: black;
            }
            QMenu::item:selected {
                background-color: #f0f0f0;
                color: black;
            }
        """)


class StreakWidget(QFrame):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedSize(320, 65)
        self.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
                border-radius: none;
            }
        """)

        streak_layout = QHBoxLayout(self)
        self.setFixedSize(280, 35)
        streak_layout.setContentsMargins(5, 0, 0, 0)   
        streak_layout.setSpacing(0)                     

        self.streak_icon = QLabel()
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon", "fire1.png")
        pixmap_fire = QPixmap(icon_path)
        self.streak_icon.setPixmap(pixmap_fire.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.streak_entry_txt = QLabel("DAY - 1/7 COMPLETED")
        self.streak_entry_txt.setStyleSheet("""
            font-size: 24px;
            color: #000000;
            font-family: 'Dreaming Outloud AllCaps';
            font-weight: bold;
            border: none;
            background: transparent;
        """)
        
        streak_layout.addStretch()
        streak_layout.addWidget(self.streak_icon)
        streak_layout.addWidget(self.streak_entry_txt)
        streak_layout.addStretch()

    def update_streak(self, count):
        self.streak_entry_txt.setText(f"DAY - {count}/7 COMPLETED")


class ProgressBarWidget(QProgressBar):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setMinimumWidth(300) 
        self.setMaximumWidth(600) 
        self.setFixedSize(350, 30)
        
        self.setValue(14)        
        self.setTextVisible(False)
        self.setStyleSheet("""
            QProgressBar {
                background-color: #f7f2b3;
                border-radius: 15px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #9AB3D5;
                border-radius: 15px;
            }
        """)

    def update_progress(self, streak_count):
        percentage = min(100, (streak_count / 7) * 100)
        self.setValue(int(percentage))
