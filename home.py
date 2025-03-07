from PyQt5.QtWidgets import  QMainWindow, QGraphicsDropShadowEffect
from PyQt5 import uic
from PyQt5.QtGui import QColor, QPainter, QTextCharFormat, QColor, QTextCursor
from PyQt5.QtCore import Qt, QPoint,QEvent
from PyQt5.QtWidgets import QButtonGroup ,QFrame, QVBoxLayout,QLabel,QApplication,QCalendarWidget,QPushButton,QFileDialog,QMessageBox
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime, timedelta
import ctypes


class Ui_HomeWindow(QMainWindow):

    _isClick = None

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/home.ui",self)
        self.setAndRun()

    def setAndRun(self):
        self.setMinimumSize(150, 50)
        self.show()
    
   
    