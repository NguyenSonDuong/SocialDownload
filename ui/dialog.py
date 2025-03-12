from PyQt5 import uic
from PyQt5.QtGui import QColor, QPainter, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout
import ui.controller.uicontroller as controller
from config.setting import Setting, OrderType, Social, TypeID, TypeChannel, TypeDownloadDoyin, TypeDownloadYoutube
import json
from datetime import datetime, timedelta
from social import SocialThread
from common.globalstate import GlobalState
import os


class DialogOverlay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(parent.size())
        self.setUIUX()

    def setUIUX(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.main_layout = QVBoxLayout(self)
        self.frame = QFrame(self)
        uic.loadUi("ui/dialog.ui",self.frame)
        self.frame.setFixedSize(650, 490)
        layout = QVBoxLayout(self.frame)
        self.main_layout.addWidget(self.frame, alignment=Qt.AlignCenter)
        
        self.btnChayAn.clicked.connect(self.hide_overlay)

    def setOverlayGeometry(self, target_widget):
        self.setGeometry(target_widget.geometry())  
    def appEndLog():
        self.txtLog.append("");
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150))
    def show_overlay(self):
        self.setVisible(True)  # Hiện overlay

    def hide_overlay(self):
        self.setVisible(False)  # Ẩn overlay