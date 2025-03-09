from PyQt5.QtWidgets import  QMainWindow, QGraphicsDropShadowEffect
from PyQt5 import uic
from PyQt5.QtGui import QColor, QPainter, QTextCharFormat, QColor, QTextCursor
from PyQt5.QtCore import Qt, QPoint,QEvent
from PyQt5.QtWidgets import QButtonGroup ,QFrame, QVBoxLayout,QLabel,QApplication,QCalendarWidget,QPushButton,QFileDialog,QMessageBox
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime, timedelta
import ctypes
import ui.controller.uicontroller as controller

class Ui_HomeWindow(QMainWindow):

    _isClick = None

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/home.ui",self)
        self.setAndRun()

    def setAndRun(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(150, 50)
        
        self.setupShadowsForTheme()
        shadow = QGraphicsDropShadowEffect(self.btnDouyin)
        shadow.setBlurRadius(15)  
        shadow.setOffset(3, 3)  
        shadow.setColor(QColor(0, 0, 0, 100)) 
        self.btnDouyin.setGraphicsEffect(shadow)
        self._isClick = self.btnDouyin
        self.show()


    # Event sử lý sự kiển thổng quát toàn bộ trên giao diện Filter Event

    def eventFilter(self, obj, event):
        controller.socialSelectEvent(self._isClick,obj,event)
        if obj == self.txtFromDate and event.type() == QEvent.MouseButtonPress:
            if self.calendarFrom.isVisible():
                self.calendarFrom.hide()
            else:
                # Lấy vị trí của nút trên màn hình (global position)
                button_pos = self.txtFromDate.mapToGlobal(self.txtFromDate.rect().bottomLeft())

                # Đặt CalendarWidget bên cạnh nút
                self.calendarFrom.move(button_pos.x(), button_pos.y())

                # Hiện Calendar
                self.calendarFrom.show()
            return True 

        if obj == self.txtToDate and event.type() == QEvent.MouseButtonPress:
            if self.calendarTo.isVisible():
                self.calendarTo.hide()
            else:
                # Lấy vị trí của nút trên màn hình (global position)
                button_pos = self.txtToDate.mapToGlobal(self.txtToDate.rect().bottomLeft())

                # Đặt CalendarWidget bên cạnh nút
                self.calendarTo.move(button_pos.x(), button_pos.y())

                # Hiện Calendar
                self.calendarTo.show()
            return True 
        return super().eventFilter(obj, event)
    


    def setupShadowsForTheme(self):
        controller.setShadows(self,self.layoutMain)
        controller.setShadows(self,self.layoutEditvideo)
        controller.setShadows(self,self.layoutEditColor)
        controller.setShadows(self,self.layoutEditAudio)

    # event xử lý sự kiện 
    def mouseReleaseEvent(self, event):
        self.start_pos = None
        event.accept() 
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos()  
            event.accept()  

    def mouseMoveEvent(self, event):
        if self.start_pos and event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.start_pos
            self.window().move(self.window().pos() + delta)
            self.start_pos = event.globalPos()
            event.accept()      
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            self.adjustSizeToScreen()
        super().changeEvent(event)

    def moveEvent(self, event):
        self.adjustSizeToScreen()
        super().moveEvent(event)

    def adjustSizeToScreen(self):
        self.resize(1450, 865)  