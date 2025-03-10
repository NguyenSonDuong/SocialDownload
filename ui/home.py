from PyQt5.QtWidgets import  QMainWindow, QGraphicsDropShadowEffect
from PyQt5 import uic
from PyQt5.QtGui import QColor, QPainter, QTextCharFormat, QColor, QTextCursor, QPixmap
from PyQt5.QtCore import Qt, QPoint,QEvent
from PyQt5.QtWidgets import QButtonGroup ,QFrame, QVBoxLayout,QLabel,QApplication,QCalendarWidget,QPushButton,QFileDialog,QMessageBox
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime, timedelta
import ctypes
import ui.controller.uicontroller as controller
from config.setting import Setting, OrderType, Social
class Ui_HomeWindow(QMainWindow):

    _isClick = None
    _setting = Setting()

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/home.ui",self)
        self.setAndRun()

    
    # XỬ lý sự kiện click nút RUN
    
    def setupButtonRunClick(self):



        self.btnRun.clicked.connect(self.onRunClick)

    def onRunClick(self,event):
        print("click")

    # xử lý Group radiobutom
    def setupGroupCheckbox(self):

        self.groupTypeID = QButtonGroup(self)
        self.groupTypeID.addButton(self.rdDownloadFromLink,0)
        self.groupTypeID.addButton(self.rdFullChannel,1)
        self.groupTypeID.addButton(self.rdFromKey,2)

        self.groupOrder = QButtonGroup(self)

        self.groupOrder.addButton(self.rdDownloadNewVideo,0)
        self.groupOrder.addButton(self.edDownloadTrending,1)
        self.groupOrder.addButton(self.rdDownloadOld,2)

        self.groupOrder.addButton(self.rdDownloadDate,3)
        self.groupOrder.addButton(self.rdDownloadWeek,4)
        self.groupOrder.addButton(self.rdCustomTime,5)

        self.groupYoutubeChannel = QButtonGroup(self)
        self.groupYoutubeChannel.addButton(self.rdVideoYoutube,0)
        self.groupYoutubeChannel.addButton(self.rdShortYoutube,1)
        
        self.groupTypeID.buttonClicked.connect(self.onSelectTypeDownload)
        self.groupOrder.buttonClicked.connect(self.onSelectOrder)
        self.groupYoutubeChannel.buttonClicked.connect(self.onSelectYoutubeChannel)

    def onSelectTypeDownload(self, button):
        button_id = self.groupTypeID.id(button)  
        self._setting.type_id = button_id
        print(f"Button clicked: {button.text()}, ID: {button_id}")

    def onSelectOrder(self, button):
        button_id = self.groupOrder.id(button)  
        self._setting.order_type = button_id
        if button_id == OrderType.FOR_TIME:
            self.txtFromDate.show()
            self.txtToDate.show()
        else:
            self.txtFromDate.hide()
            self.txtToDate.hide()
        print(f"Button clicked: {button.text()}, ID: {button_id}")

    def onSelectYoutubeChannel(self, button):
        button_id = self.groupYoutubeChannel.id(button)  
        self._setting.type_channel = button_id
        print(f"Button clicked: {button.text()}, ID: {button_id}")


    # Xử lý nhập thư mục lưu file
    def setupFolderSelect(self):
        self.btnSelectFolder.clicked.connect(self.onBtnSelectFolderClick)

    def onBtnSelectFolderClick(self,event):
        folder_path = QFileDialog.getExistingDirectory(self, "Chọn thư mục", "D:/")
        
        if folder_path:  # Nếu người dùng chọn thư mục
            self.txtFolderSaveVideo.setText(f"{folder_path}")

    # Xử lý nhập số lượng tải

    def setupCountDownload(self):
        self.rdDownloadAllVideo.stateChanged.connect(self.onDownloadAllChecked)

    def onDownloadAllChecked(self, state):
        if state == 2:  # Qt.Checked
            self.lbQuantityDownload.hide()
            self.txtQuatityDownload.hide()
            
        else:  # Qt.Unchecked
            self.lbQuantityDownload.show()
            self.txtQuatityDownload.show()
    # Xử lý ngày tháng 
    def showAndHideSelectDatetimePicker(self, obj,event):
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
    def setupCalendar(self):
        self.txtFromDate.hide()
        self.txtToDate.hide()
        self.calendarFrom = QCalendarWidget(self)
        self.calendarTo = QCalendarWidget(self)
        self.calendarFrom.setWindowFlags(self.calendarFrom.windowFlags() | 
                                     Qt.Popup)
        self.calendarTo.setWindowFlags(self.calendarTo.windowFlags() | 
                                     Qt.Popup)
        self.calendarFrom.clicked.connect(self.setDateCalendarFrom)
        self.calendarTo.clicked.connect(self.setDateCalendarTo)
        
        self.calendarFrom.hide()  # Ẩn khi khởi động
        self.calendarTo.hide()  # Ẩn khi khởi động
        
        self.txtFromDate.installEventFilter(self)
        self.txtToDate.installEventFilter(self)
    def setDateCalendarFrom(self, date):
        formatted_date = date.toString("dd/MM/yyyy")  # Định dạng ngày
        self.txtFromDate.setText(formatted_date)
        self.calendarFrom.hide()  # Ẩn Calendar sau khi chọn ngày
    def setDateCalendarTo(self, date):
        """Lấy ngày đã chọn và hiển thị vào LineEdit"""
        formatted_date = date.toString("dd/MM/yyyy")  # Định dạng ngày
        self.txtToDate.setText(formatted_date)
        self.calendarTo.hide()  # Ẩn Calendar sau khi chọn ngày
    # Event sử lý sự kiển thổng quát toàn bộ trên giao diện Filter Event

    def eventFilter(self, obj, event):
        self.socialSelectEvent(obj,event)
        self.showAndHideSelectDatetimePicker(obj,event)

        return super().eventFilter(obj, event)
    
    # Xử lý sự kiện chuyển Social
    def setupNavigator(self):
        self.btnDouyin.installEventFilter(self)
        self.btnYoutube.installEventFilter(self)
        self.btnFacebook.installEventFilter(self)
        self.btInstagram.installEventFilter(self)
        self.btnTwitter.installEventFilter(self)
        self.btnSnapChat.installEventFilter(self)
        self.btnQQLive.installEventFilter(self)

    def setupShadowsForTheme(self):
        controller.setShadows(self,self.layoutMain)
        controller.setShadows(self,self.layoutEditvideo)
        controller.setShadows(self,self.layoutEditColor)
        controller.setShadows(self,self.layoutEditAudio)

    def socialSelectEvent(self, obj, event):
        if event.type() == QEvent.Enter:  # Khi di chuột vào
            if self._isClick != obj:
                controller.setShadows(self,obj)
        elif event.type() == QEvent.Leave: 
            if self._isClick != obj:
                obj.setGraphicsEffect(None)
        elif event.type() == QEvent.MouseButtonPress:
            if self._isClick != obj:
                if self._isClick != None:
                    self._isClick.setGraphicsEffect(None) 
                controller.setShadows(self,obj) 
                self._isClick = obj
                self.swichSocial()

    def swichSocial(self):
        if self._isClick == self.btnDouyin:
            self._setting.social = Social.DOUYIN
            pixmap = QPixmap("ui/img/DouyinChar.png")  # Đường dẫn ảnh
            self.lbLogoSocial.setPixmap(pixmap)

            self.txtUrl.setPlaceholderText("https://www.douyin.com/user/...")
            self.rdDownloadOld.setEnabled(False)
            self.rdDownloadOld.setChecked(False)
        if self._isClick == self.btnYoutube:
            self._setting.social = Social.YOUTUBE
            pixmap = QPixmap("ui/img/YoutubeChart.png")  # Đường dẫn ảnh
            self.lbLogoSocial.setPixmap(pixmap)

            self.txtUrl.setPlaceholderText("https://www.youtube.com/...")
            self.rdDownloadOld.setEnabled(True)

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



    def setAndRun(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(150, 50)
        self.setupNavigator()
        self.setupShadowsForTheme()
        self.setupGroupCheckbox()
        self.setupCalendar()
        self.setupCountDownload()
        self.setupFolderSelect()
        controller.setShadows(self,self.btnDouyin)


        self._isClick = self.btnDouyin
        self.show()
