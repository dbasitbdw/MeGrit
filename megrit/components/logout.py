from PyQt5.QtWidgets import QMessageBox

class Logout:
    @staticmethod
    def confirm(parent):
        msg = QMessageBox(parent)
        msg.setWindowTitle('Logout')
        msg.setText('Apakah anda yakin ingin keluar?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setStyleSheet("""
            QMessageBox { background-color: white; }
            QLabel { color: #000000; }
        """)
        
        btn_style = """
            QPushButton { 
                color: black !important; 
                background-color: #e0e0e0; 
                border: 1px solid #999999;
                padding: 5px 15px;
                min-width: 60px;
            }
            QPushButton:hover { background-color: #c0c0c0; }
        """
        
        yes_btn = msg.button(QMessageBox.Yes)
        no_btn = msg.button(QMessageBox.No)
        
        if yes_btn:
            yes_btn.setStyleSheet(btn_style)
        if no_btn:
             no_btn.setStyleSheet(btn_style)
        
        reply = msg.exec_()
        return reply == QMessageBox.Yes
