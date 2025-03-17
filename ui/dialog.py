from PyQt5 import uic
from PyQt5.QtGui import QColor, QPainter, QColor,QTextCharFormat, QTextCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from common.globalstate import GlobalStatePause,GlobalStateRun
import logging
logging.basicConfig(filename="error.log", level=logging.ERROR)

class DialogOverlay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            self.resize(parent.size())
            self.setUIUX()
            self.isRun = GlobalStateRun()
            self.isPause = GlobalStatePause()
        except Exception as e:
            logging.error(e)
        

    def setUIUX(self):
        try:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setAttribute(Qt.WA_DeleteOnClose)
            self.main_layout = QVBoxLayout(self)
            self.frame = QFrame(self)
            self.frame.setFixedSize(650, 490)
            uic.loadUi("ui/dialog.ui",self.frame)
            layout = QVBoxLayout(self.frame)
            self.main_layout.addWidget(self.frame, alignment=Qt.AlignCenter)

            self.frame.btnChayAn.clicked.connect(self.hide_overlay)
            self.frame.btnHuyTai.clicked.connect(self.btnHuyTaiOnClicked)
            self.frame.btnDung.clicked.connect(self.btnDungClicked)
        except Exception as e:
            logging.error(e)
        
    def btnHuyTaiOnClicked(self, event):
        self.isRun.set_value(False)
    def btnDungClicked(self, event):
        self.isPause.set_value(not self.isPause.get_value())
        
    def append_text(self, text, color):
        """ Thêm văn bản với màu tùy chỉnh """
        cursor = self.frame.txtLog.textCursor()  
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))  

        cursor.movePosition(QTextCursor.End) 
        cursor.mergeCharFormat(fmt)  
        cursor.insertText(text + "\n") 
        
    def setOverlayGeometry(self, target_widget):
        self.setGeometry(target_widget.geometry())  
        
    def log(self,message,color = "black"):
        self.append_text(message,color)
    def setProcess(self,pbTienTrinh,maximum = 100):
        self.frame.pbTienTrinh.setValue(int(pbTienTrinh))  # Cập nhật giá trị
        self.frame.pbTienTrinh.setMaximum(maximum)
    def setProcessPhu(self,pbTienTrinh,maximum = 100):
        self.frame.pbTienTrinhPhu.setValue(int(pbTienTrinh))  # Cập nhật giá trị
        self.frame.pbTienTrinhPhu.setMaximum(maximum)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150))
    def show_overlay(self):
        self.setVisible(True)  # Hiện overlay

    def hide_overlay(self):
        self.setVisible(False)  # Ẩn overlay