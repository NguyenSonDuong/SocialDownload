from PyQt5.QtWidgets import  QMainWindow, QGraphicsDropShadowEffect
from PyQt5 import uic
from PyQt5.QtGui import QColor, QPainter, QTextCharFormat, QColor, QTextCursor
from PyQt5.QtCore import Qt, QPoint,QEvent
from PyQt5.QtWidgets import QButtonGroup ,QFrame, QVBoxLayout,QLabel,QApplication,QCalendarWidget,QPushButton,QFileDialog,QMessageBox
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime, timedelta
import ctypes


def socialSelectEvent(_isClick, obj, event):
    if event.type() == QEvent.Enter:  # Khi di chuột vào
        if _isClick != obj:
            shadow = QGraphicsDropShadowEffect(obj)
            shadow.setBlurRadius(15)  
            shadow.setOffset(3, 3)  
            shadow.setColor(QColor(0, 0, 0, 100)) 
            obj.setGraphicsEffect(shadow)  
    elif event.type() == QEvent.Leave: 
        if _isClick != obj:
            obj.setGraphicsEffect(None)
    elif event.type() == QEvent.MouseButtonPress:
        if _isClick != obj:
            if _isClick != None:
                _isClick.setGraphicsEffect(None) 
            shadow = QGraphicsDropShadowEffect(obj)
            shadow.setBlurRadius(15)  
            shadow.setOffset(3, 3)  
            shadow.setColor(QColor(0, 0, 0, 100)) 
            obj.setGraphicsEffect(shadow)  
            _isClick = obj
def setShadows(parter,chill):
    shadow = QGraphicsDropShadowEffect(parter)
    shadow.setBlurRadius(20)
    shadow.setOffset(2, 2)
    shadow.setColor(QColor(0, 0, 0, 80))
    chill.setGraphicsEffect(shadow)