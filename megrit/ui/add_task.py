from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QButtonGroup, QComboBox, QDateEdit, QTimeEdit,
    QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate, QTime, pyqtSignal, QSize, QEvent
from megrit.components.time_picker import TimePickerDialog
import os

class AddTaskPage(QWidget):

    task_added = pyqtSignal()
    cancelled = pyqtSignal()

    def __init__(self, task_manager=None, parent=None):
        super().__init__(parent)
        self.task_manager = task_manager
        self.setStyleSheet("""
            QWidget {
                background-color: #fffaf0;
                color: #000000;
            }
            QMessageBox {
                background-color: #fffaf0;
            }
            QMessageBox QLabel {
                color: #000000;
            }
            QCalendarWidget QWidget {
                 background-color: white; 
                 alternate-background-color: #f0f0f0;
                 color: black;
            }
            QCalendarWidget QToolButton {
                color: black;
            }
        """)
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the add task UI"""
        self.content_layout = QVBoxLayout(self)
    def setup_ui(self):
        """Initialize the add task UI"""
        self.content_layout = QVBoxLayout(self)
        self.content_layout.setContentsMargins(30, 20, 30, 10) 
        self.content_layout.setAlignment(Qt.AlignTop)
      
        self.add_label = QLabel("Add Activity")
        self.add_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                color: #000000;
                font-family: 'Dreaming Outloud AllCaps';
                font-weight: bold;
            }
        """)
        self.content_layout.addWidget(self.add_label)

        self.body_container = QWidget()
        self.body_layout = QVBoxLayout(self.body_container)
        self.body_layout.setContentsMargins(0, 10, 0, 0)
        self.body_layout.setSpacing(15)
        self.body_layout.setAlignment(Qt.AlignTop)

        self.add_input = QLineEdit()
        self.add_input.setPlaceholderText("Write your activity here...")
        self.add_input.setFixedSize(550, 60)
        self.add_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(177, 200, 239, 0.25);
                border: 2px solid rgba(0,0,0,0.25);
                border-radius: 15px;
                padding-left: 20px;
                font-family: 'Poppins';
                font-size: 16px;
                color: #000000;
            }
        """)
        self.body_layout.addWidget(self.add_input, alignment=Qt.AlignCenter)
        self.content_layout.addWidget(self.body_container)

        self.category_txt = QLabel("Select Category")
        self.category_txt.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #000000;
                font-family: 'Poppins';
                background: transparent;
            }
        """)
        self.body_layout.addWidget(self.category_txt, alignment=Qt.AlignCenter)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.setSpacing(20)
        self.btn_layout.setAlignment(Qt.AlignCenter)
        self.category_group = QButtonGroup(self)
        self.category_group.setExclusive(True)
        
        categories = ["work", "study", "sport", "personal", "money"]
        
        for cat in categories:
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setFixedSize(60, 60)
            btn.setProperty("category", cat)
            
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon", f"{cat}.png")
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
                btn.setIconSize(QSize(35, 35))
            
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(177, 200, 239, 0.25);
                    border: 2px solid rgba(0,0,0,0.25);
                    border-radius: 30px; 
                }
                QPushButton:checked {
                    background-color: rgba(177, 200, 239, 0.25);
                    border: 3px solid #465375;
                }
            """)
            
            self.category_group.addButton(btn)
            self.btn_layout.addWidget(btn)
         
            if cat == "work":
                btn.setChecked(True)

        self.body_layout.addLayout(self.btn_layout)

        self.prio_layout = QHBoxLayout()
        self.prio_layout.setContentsMargins(50, 10, 0, 0)
        self.prio_layout.setSpacing(10)
        
        self.prio_txt = QLabel("Setting Priority: ")
        self.prio_txt.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #000000;
                font-family: 'Poppins';
                background: transparent;
            }
        """)
        self.prio_layout.addWidget(self.prio_txt)

        self.prio_dropdown = QComboBox()
        self.prio_dropdown.addItems(["Emergency", "High", "Low", "Routine"])
        self.prio_dropdown.setFixedSize(250, 35)
        self.prio_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #FFF9E3; 
                border: 2px solid #C4C4C4;
                border-radius: 17px; 
                padding-left: 20px; 
                font-family: 'Poppins';
                font-size: 16px;
                color: #000000;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center left; 
                width: 30px;
                border: none;
            }
        """)
        self.prio_layout.addWidget(self.prio_dropdown)
        self.prio_layout.addStretch()
        self.body_layout.addLayout(self.prio_layout)

        self.date_layout = QHBoxLayout()
        self.date_layout.setContentsMargins(50, 10, 0, 0)
        self.date_layout.setSpacing(10)
        
        self.date_txt = QLabel("Set Date          : ")
        self.date_txt.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #000000;
                font-family: 'Poppins';
                background: transparent;
            }
        """)
        
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True) 
        self.date_input.setDate(QDate.currentDate()) 
        self.date_input.setFixedSize(160, 35)
        self.date_input.setStyleSheet("""
            QDateEdit {
                background-color: #FFF9E3;
                border: 2px solid #C4C4C4;
                border-radius: 17px;
                padding-left: 15px; 
                font-family: 'Poppins';
                font-size: 16px;
                color: #000000;
            }
            QDateEdit::up-button, QDateEdit::down-button {
                width: 0px; 
                border: none;
                background: transparent;
            }
        """)

        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())
        self.time_input.setDisplayFormat("HH:mm")
        self.time_input.setFixedSize(100, 35) 
        self.time_input.setReadOnly(True) 
        
        self.time_input.installEventFilter(self)
        for child in self.time_input.children():
            if isinstance(child, QLineEdit):
                child.installEventFilter(self)
        
        self.time_input.setStyleSheet("""
            QTimeEdit {
                background-color: #FFF9E3;
                border: 2px solid #C4C4C4;
                border-radius: 17px;
                font-family: 'Poppins';
                font-size: 16px;
                color: #000000;
                qproperty-alignment: 'AlignCenter';
            }
            /* Hide buttons completely */
            QTimeEdit::up-button, QTimeEdit::down-button {
                width: 0px;
                border: none;
                background: transparent;
            }
        """)
        
        self.date_layout.addWidget(self.date_txt)
        self.date_layout.addWidget(self.date_input)
        self.date_layout.addWidget(self.time_input)
        self.date_layout.addStretch()
        self.body_layout.addLayout(self.date_layout)

        self.btns_layout = QHBoxLayout()
        self.btns_layout.setContentsMargins(50, 20, 0, 0)
        self.btns_layout.setSpacing(20)

        self.btn_sv = QPushButton(" SAVE")
        self.btn_sv.setFixedSize(120, 38)
        self.setup_btn_icon(self.btn_sv, "save.png")
        self.btn_sv.setStyleSheet("""
            QPushButton {
                background-color: #e4efd2;
                border: 2px solid rgba(0,0,0,0.25);
                border-radius: 8px;
                font-family: 'Dreaming Outloud AllCaps';
                font-size: 22px;
                font-weight: bold;
                padding-left: 5px;
                font-weight: bold;
                padding-left: 5px;
                text-align: left;
                color: #000000;
            }
        """)
        self.btn_sv.clicked.connect(self.save_task)

        self.btn_cc = QPushButton(" CANCEL")
        self.btn_cc.setFixedSize(140, 38)
        self.setup_btn_icon(self.btn_cc, "cancel.png")
        self.btn_cc.setStyleSheet("""
            QPushButton {
                background-color: #f3c3c5;
                border: 2px solid rgba(0,0,0,0.25);
                border-radius: 8px;
                font-family: 'Dreaming Outloud AllCaps';
                font-size: 22px;
                font-weight: bold;
                padding-left: 5px;
                padding-left: 5px;
                text-align: left;
                color: #000000;
            }
        """)
        self.btn_cc.clicked.connect(self.cancel_task)

        self.btns_layout.addWidget(self.btn_sv)
        self.btns_layout.addWidget(self.btn_cc)
        self.btns_layout.addStretch()
        self.body_layout.addLayout(self.btns_layout)
        
        self.content_layout.addStretch()

    def setup_btn_icon(self, btn, icon_name):
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon", icon_name)
        if os.path.exists(icon_path):
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(25, 25))

    def save_task(self):
        """Save task to TaskManager"""
        description = self.add_input.text().strip()
        if not description:
            QMessageBox.warning(self, "Input Error", "Please enter activity description!")
            return

        selected_btn = self.category_group.checkedButton()
        category = selected_btn.property("category") if selected_btn else "work"
  
        qdate = self.date_input.date()
        qtime = self.time_input.time()
        
        task_data = {
            'description': description,
            'category': category,
            'priority': self.prio_dropdown.currentText(),
            'status': 'Pending',
            'scheduled_date': qdate.toString("dd/MM/yy"),
            'scheduled_time': qtime.toString("HH.mm")
        }
        
        if self.task_manager:
            self.task_manager.add_task(task_data)
            self.task_added.emit()
            self.reset_form()
        else:
            print("Task Manager not connected!")

    def cancel_task(self):
        """Cancel and reset form"""
        self.reset_form()
        self.cancelled.emit()
    
    def reset_form(self):
        """Reset all input fields"""
        self.add_input.clear()
        buttons = self.category_group.buttons()
        if buttons:
            buttons[0].setChecked(True)
        
        self.prio_dropdown.setCurrentIndex(0)
        self.date_input.setDate(QDate.currentDate())
        self.time_input.setTime(QTime.currentTime())

    def eventFilter(self, source, event):
        if (source == self.time_input or source in self.time_input.children()) and event.type() == QEvent.MouseButtonPress:
            self.open_time_picker()
            return True
        return super().eventFilter(source, event)

    def open_time_picker(self):
        """Open custom time picker dialog"""
        dialog = TimePickerDialog(self, self.time_input.time())
        if dialog.exec_():
            new_time = dialog.get_time()
            self.time_input.setTime(new_time)
