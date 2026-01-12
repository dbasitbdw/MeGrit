from PyQt5.QtCore import QObject, QTimer, pyqtSignal

class PomodoroTimer(QObject):
    timer_tick = pyqtSignal(str, float) 
    mode_changed = pyqtSignal(bool)    
    finished = pyqtSignal()
 
    WORK_TIME = 30 * 60 
    BREAK_TIME = 5 * 60 

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        
        self.running = False
        self.is_break = False
        self.remaining = float(self.WORK_TIME)
        self.total_time = float(self.WORK_TIME)
        self.tick_interval = 100 
        self.decrement = 0.1 

    def start(self):
        if not self.running:
            if self.remaining == self.WORK_TIME and not self.is_break:
                self.total_time = float(self.WORK_TIME)
            
            self.running = True
            self.timer.start(self.tick_interval)

    def pause(self):
        if self.running:
            self.running = False
            self.timer.stop()

    def reset(self):
        self.running = False
        self.timer.stop()
        self.is_break = False
        self.remaining = float(self.WORK_TIME)
        self.total_time = float(self.WORK_TIME)
        self._update_signals()

    def _tick(self):
        if self.remaining > 0:
            self.remaining -= self.decrement
            
            if self.remaining < 0:
                self.remaining = 0
           
            if not self.is_break and abs(self.remaining - self.BREAK_TIME) < 0.05:
                self.remaining = float(self.BREAK_TIME)
                self._switch_mode()
            elif self.is_break and self.remaining <= 0.05:
                self.remaining = 0
                self.finished.emit()
                self.reset()
                return

            self._update_signals()
        else:
            self.finished.emit()
            self.reset()

    def _switch_mode(self):
        if not self.is_break:
            self.is_break = True
            self.total_time = float(self.BREAK_TIME) 
            self.mode_changed.emit(self.is_break)
            self._update_signals()

    def _update_signals(self):
    
        import math
        display_seconds = math.ceil(self.remaining)
        m, s = divmod(display_seconds, 60)
        formatted_time = f"{m:02}:{s:02}"
     
        if self.total_time > 0:
            progress = self.remaining / self.total_time
        else:
            progress = 0
            
        self.timer_tick.emit(formatted_time, progress)
