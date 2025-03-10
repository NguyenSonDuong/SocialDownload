from PyQt5.QtWidgets import  QMainWindow, QGraphicsDropShadowEffect
from PyQt5 import uic
from PyQt5.QtGui import QColor, QPainter, QTextCharFormat, QColor, QTextCursor
from PyQt5.QtCore import Qt, QPoint,QEvent
from PyQt5.QtWidgets import QButtonGroup ,QFrame, QVBoxLayout,QLabel,QApplication,QCalendarWidget,QPushButton,QFileDialog,QMessageBox
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime, timedelta
import ctypes
from config.setting import TypeID,Social,TypeDownloadYoutube,TypeChannel,TypeDownloadDoyin
import re
def validateUrlYoutube(url,setting):
    if not url.startswith("https://www.youtube.com/"):
        return False
    if setting.type_id == TypeID.CHANNEL:
        pattern = r"^(https?://)?(www\.)?youtube\.com/(channel/UC[a-zA-Z0-9_-]{21,24}|@[\w-]+)(/.*)?$"
        return re.match(pattern, url) is not None


def setShadows(parter,chill):
    shadow = QGraphicsDropShadowEffect(parter)
    shadow.setBlurRadius(20)
    shadow.setOffset(2, 2)
    shadow.setColor(QColor(0, 0, 0, 80))
    chill.setGraphicsEffect(shadow)