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
from bs4 import BeautifulSoup
import requests

# validate and get id youtube
def validateUrlYoutube(url,setting):
    if not url.startswith("https://www.youtube.com/"):
        return None
    if setting.type_id == TypeID.CHANNEL:
        type_link, idOrUser  = getUsernameOrID(url)
        if not idOrUser or not type_link:
            return None
        if type_link == "username":
            print(idOrUser)
            idOrUser = GetIdChannel(idOrUser)
        return idOrUser
    if setting.type_id == TypeID.LINK:
        type_link, idLink  = getIdLink(url)  
        if not type_link or not idLink:
            return None
        return idLink
    return None
def GetIdChannel(url):
    try:
        response = requests.get(f"https://www.youtube.com/@{url}")
        soup = BeautifulSoup(response.text, "html.parser")
        meta_tag = soup.find("meta", {"property": "al:ios:url"})
        if meta_tag:
            href_value = meta_tag.get("content")
            pattern = r"www\.youtube\.com/channel/([\w-]+)"
            match = re.search(pattern, href_value)

            if match:
                channel_id = match.group(1)
                return channel_id
            else:
                return None
        else:
            return None
    except Exception as ex:
        return None
def getIdLink(url):
    patterns = [
        (r"youtube\.com/watch\?v=([a-zA-Z0-9_-]+)", "video"),
        (r"youtube\.com/shorts/([a-zA-Z0-9_-]+)", "shorts"),
        (r"youtu\.be/([a-zA-Z0-9_-]+)", "video")  # Dạng rút gọn
    ]

    for pattern, type_ in patterns:
        match = re.search(pattern, url)
        if match:
            return type_, match.group(1)

    return None, None
def getUsernameOrID(url):
    patterns = [
        (r"youtube\.com/channel/([a-zA-Z0-9_-]+)", "channel_id"),
        (r"youtube\.com/c/([^/?]+)", "username"),
        (r"youtube\.com/@([^/?]+)", "username")
    ]
    for pattern, type_ in patterns:
        match = re.search(pattern, url)
        if match:
            return type_, match.group(1)
    return None, None

# validate
def validateDate(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")  # Định dạng chuẩn
        return True
    except ValueError:
        return False
def validateUrl(url):
    pattern = re.compile(
        r'^(https?|ftp)://'  # http:// hoặc https:// hoặc ftp://
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6}|'  # Domain (ví dụ: google.com)
        r'localhost|'  # Cho phép localhost
        r'\d{1,3}(\.\d{1,3}){3})'  # Hoặc IP (ví dụ: 192.168.1.1)
        r'(:\d+)?'  # Cổng (ví dụ: :80)
        r'(/[-A-Za-z0-9+&@#/%?=~_|!:,.;]*)?'  # Đường dẫn
        r'(\?[A-Za-z0-9+&@#/%=~_|!:,.;]*)?$'  # Query string (nếu có)
    )
    return re.match(pattern, url) is not None

#UI edit
def setShadows(parter,chill):
    shadow = QGraphicsDropShadowEffect(parter)
    shadow.setBlurRadius(20)
    shadow.setOffset(2, 2)
    shadow.setColor(QColor(0, 0, 0, 80))
    chill.setGraphicsEffect(shadow)

# validate and get id douyin
def validateUrlDouyin(url,setting):
    if setting.type_id == TypeID.CHANNEL:
        idOrUser  = validateUserDoutin(url)
        return idOrUser
    if setting.type_id == TypeID.LINK:
        idLink  = validatePostlDouyin(url)  
        if idLink:
            idLink = getIDFromShortLink(idLink)
        else:
            video_id_match = re.search(r"/video/(\d+)", url)
            idLink = video_id_match.group(1) if video_id_match else None
        return idLink
    return None

def validateUrlWeibo(url):
    match = re.search(r"weibo\.com/u/(\d+)", url)

    if match:
        user_id = match.group(1)
        return user_id
    return None

def validateUserDoutin(url):
    match = re.search(r'douyin\.com/user/([\w-]+)', url)  # Lấy ID sau "/user/"
    if match:
        return match.group(1)
    return None
def validatePostlDouyin(url):
    match = re.search(r"https://v\.douyin\.com/([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None
def getIDFromShortLink(id):
    response = requests.head(f"https://v.douyin.com/{id}", allow_redirects=True)
    full_url = response.url
    video_id_match = re.search(r"/video/(\d+)", full_url)
    return video_id_match.group(1) if video_id_match else None