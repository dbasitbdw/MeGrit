from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QRectF, QSize
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QFontDatabase, QIcon
from PyQt5.QtMultimedia import QSound
import os
from megrit.logic.pomodoro_timer import PomodoroTimer

class ProgressCircle(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 1.0
        self.setMinimumSize(480, 480) 

    def set_progress(self, value):
        self.progress = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        center_x = width // 2
        center_y = height // 2
        
        stroke = 60 
        radius = min(width, height) // 2 - stroke 
        
        rect = QRectF(center_x - radius, center_y - radius, radius * 2, radius * 2)

        COLOR_YELLOW = "#f6efb3"
        COLOR_BLUE = "#bcd2f5"

        pen_base = QPen(QColor(COLOR_YELLOW), stroke, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen_base)
        painter.drawArc(rect, 0, 360 * 16)

        pen_progress = QPen(QColor(COLOR_BLUE), stroke, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen_progress)
        
        span_angle = int(360 * 16 * self.progress)
        painter.drawArc(rect, 90 * 16, -span_angle)


class PomodoroPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer_logic = PomodoroTimer(self)
        self.load_fonts()
        self.setStyleSheet("background-color: #fef8e9;")
        self.init_ui()
        self.connect_signals()

    def load_fonts(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
        
        font_path_dreaming = os.path.join(base_path, "assets", "font", "dreaming-outloud-allcaps-regular.otf")
        id_dreaming = QFontDatabase.addApplicationFont(font_path_dreaming)
        if id_dreaming != -1:
            self.font_family_dreaming = QFontDatabase.applicationFontFamilies(id_dreaming)[0]
        else:
            print(f"Failed to load font: {font_path_dreaming}")
            self.font_family_dreaming = "Sans Serif"

        font_path_poppins = os.path.join(base_path, "assets", "font", "poppins.medium.ttf")
        id_poppins = QFontDatabase.addApplicationFont(font_path_poppins)
        if id_poppins != -1:
            self.font_family_poppins = QFontDatabase.applicationFontFamilies(id_poppins)[0]
        else:
            print(f"Failed to load font: {font_path_poppins}")
            self.font_family_poppins = "Sans Serif"

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 20, 30, 30)

        self.header_label = QLabel("Pomodoro")
        font_header = QFont(self.font_family_poppins, 20)
        self.header_label.setFont(font_header)
        self.header_label.setStyleSheet("color: black;")
        self.header_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.main_layout.addWidget(self.header_label)

        self.main_layout.addStretch()

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        
        self.circle_container = ProgressCircle(self)
        self.circle_inner_layout = QVBoxLayout(self.circle_container)
        self.circle_inner_layout.setAlignment(Qt.AlignCenter)
        self.circle_inner_layout.setSpacing(10)

        self.mode_label = QLabel("WORK")
        font_mode = QFont(self.font_family_dreaming, 32) 
        self.mode_label.setFont(font_mode)
        self.mode_label.setStyleSheet("color: black; letter-spacing: 2px; background: transparent;")
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.circle_inner_layout.addWidget(self.mode_label)
        self.timer_widget = QWidget()
        self.timer_widget.setStyleSheet("background: transparent;")
        
        self.timer_layout = QHBoxLayout(self.timer_widget)
        self.timer_layout.setContentsMargins(0, 0, 0, 0)
        self.timer_layout.setSpacing(8) 
        self.timer_layout.setAlignment(Qt.AlignCenter)

        font_timer = QFont(self.font_family_dreaming, 44)
        
        self.lbl_min = QLabel("30")
        self.lbl_min.setFont(font_timer)
        self.lbl_min.setStyleSheet("color: black; background: transparent;")
        self.lbl_min.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_min.setFixedWidth(90)

        self.lbl_colon = QLabel(":")
        self.lbl_colon.setFont(font_timer)
        self.lbl_colon.setStyleSheet("color: black; background: transparent;")
        self.lbl_colon.setAlignment(Qt.AlignCenter)
        self.lbl_colon.setFixedWidth(35) 

        self.lbl_sec = QLabel("00")
        self.lbl_sec.setFont(font_timer)
        self.lbl_sec.setStyleSheet("color: black; background: transparent;")
        self.lbl_sec.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lbl_sec.setFixedWidth(90)

        self.timer_layout.addWidget(self.lbl_min)
        self.timer_layout.addWidget(self.lbl_colon)
        self.timer_layout.addWidget(self.lbl_sec)

        self.circle_inner_layout.addWidget(self.timer_widget)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.setAlignment(Qt.AlignCenter)
        self.btn_layout.setSpacing(20)

        self.btn_start = QPushButton()
        self.btn_start.setFixedSize(55, 55)
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
        
        start_icon_path = os.path.join(base_path, "assets", "icon", "btn_start.png")
        self.btn_start.setIcon(QIcon(start_icon_path))
        self.btn_start.setIconSize(QSize(55, 55)) 
        self.btn_start.setStyleSheet("border: none; background: transparent;")
        self.btn_start.setCursor(Qt.PointingHandCursor)
        self.btn_start.clicked.connect(self.toggle_timer)
        self.btn_layout.addWidget(self.btn_start)

        self.btn_reset = QPushButton()
        self.btn_reset.setFixedSize(45, 45) 
        reset_icon_path = os.path.join(base_path, "assets", "icon", "btn_reset.png")
        self.btn_reset.setIcon(QIcon(reset_icon_path))
        self.btn_reset.setIconSize(QSize(45, 45)) 
        self.btn_reset.setStyleSheet("border: none; background: transparent;")
        self.btn_reset.setCursor(Qt.PointingHandCursor)
        self.btn_reset.clicked.connect(self.reset_timer)
        self.btn_layout.addWidget(self.btn_reset)
        
        self.circle_inner_layout.addLayout(self.btn_layout)
        
        h_layout.addWidget(self.circle_container)
        h_layout.addStretch()

        self.main_layout.addLayout(h_layout)

        self.main_layout.addStretch()

    def connect_signals(self):
        self.timer_logic.timer_tick.connect(self.update_timer_ui)
        self.timer_logic.mode_changed.connect(self.update_mode_icon)
        self.timer_logic.finished.connect(self.on_finished)

    def toggle_timer(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if self.timer_logic.running:
            self.timer_logic.pause()
            self.btn_start.setIcon(QIcon(os.path.join(base_path, "assets", "icon", "btn_start.png")))
        else:
            self.timer_logic.start()
            self.btn_start.setIcon(QIcon(os.path.join(base_path, "assets", "icon", "btn_pause.png")))

    def reset_timer(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.timer_logic.reset()
        self.btn_start.setIcon(QIcon(os.path.join(base_path, "assets", "icon", "btn_start.png")))
        self.update_timer_ui("30:00", 1.0) 
        self.mode_label.setText("WORK")

    def update_timer_ui(self, time_str, progress):
        parts = time_str.split(':')
        if len(parts) == 2:
            m = parts[0].strip()
            s = parts[1].strip()
            self.lbl_min.setText(m.zfill(2)) 
            self.lbl_sec.setText(s.zfill(2))
        
        self.circle_container.set_progress(progress)

    def update_mode_icon(self, is_break):
        text = "REST" if is_break else "WORK"
        self.mode_label.setText(text)
        
        if is_break:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sound_path = os.path.join(base_path, "assets", "sound", "sound_break.wav")
            QSound.play(sound_path)

    def on_finished(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.btn_start.setIcon(QIcon(os.path.join(base_path, "assets", "icon", "btn_start.png")))
        sound_path = os.path.join(base_path, "assets", "sound", "sound_finish.wav")
        QSound.play(sound_path)
