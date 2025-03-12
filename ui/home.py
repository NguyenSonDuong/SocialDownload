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
from config.setting import Setting, OrderType, Social, TypeID, TypeChannel, TypeDownloadDoyin, TypeDownloadYoutube
import json
from datetime import datetime, timedelta
from social import SocialThread
from common.globalstate import GlobalState
from common.status import Status
import os
from ui.dialog import DialogOverlay

class Ui_HomeWindow(QMainWindow):

    _isClick = None
    _setting = Setting()

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/home.ui",self)
        self.dialogProcess = DialogOverlay(self)
        self.setAndRun()
        self.dialogProcess.hide_overlay()
        self.dialogProcess.setOverlayGeometry(self.centralwidget) 

    
    # XỬ lý sự kiện click nút RUN
    
    def validateInputSetting(self):
        url = self.txtUrl.text()
        if not url or url == "":
            QMessageBox.information(self,"Cảnh báo","Vui lòng nhập url")
            return False
        if self._setting.social != Social.DOUYIN and not self.rdDownloadFromLink.isChecked():
            if not controller.validateUrl(url):
                QMessageBox.information(self,"Cảnh báo","Hãy nhập đúng định dạng url")
                return False
        if self.rdFullChannel.isChecked():
            if self.rdCustomTime.isChecked():
                if not self.txtFromDate or not self.txtToDate:
                    QMessageBox.information(self,"Cảnh báo","Hãy nhập đầy đủ ngày bắt đầu và kết thúc")
                    return False
                if not controller.validateDate(self.txtFromDate.text()) or not controller.validateDate(self.txtToDate.text()):
                    QMessageBox.information(self,"Cảnh báo","Hãy nhập đúng định dạng ngày tháng có bao gồm cả số 0")
                    return False
            if not self.rdDownloadAllVideo.isChecked():
                if not self.txtQuatityDownload.text() or self.txtQuatityDownload.text() == "":
                    QMessageBox.information(self,"Cảnh báo","Hãy nhập số lượng muốn tải nếu muốn tải hết vui lòng click vào ô tải toàn bộ")
                    return False
                if not self.txtQuatityDownload.text().isdigit():
                    QMessageBox.information(self,"Cảnh báo","Hãy nhập đúng định dạng cảu số lượng video")
                    return False
                
        if not self.txtFolderSaveVideo.text() or self.txtFolderSaveVideo.text() == "":
            QMessageBox.information(self,"Cảnh báo","Hãy nhập hoặc chọn đường dẫn")
            return False
        return True

    def setupValueSetting(self):
        
        if self._setting.social == Social.YOUTUBE:
            self._setting.id = controller.validateUrlYoutube(self.txtUrl.text(),self._setting)
        else:
            self._setting.id = controller.validateUrlDouyin(self.txtUrl.text(),self._setting)
            
        if not self._setting.id or self._setting.id == "":
            QMessageBox.information(self,"Cảnh báo","Sai định dạng link vui lòng kiểm tra mạng xã hội và cách tải")
            raise ValueError("Sai định dạng link vui lòng kiểm tra mạng xã hội và cách tải");
        
        if self._setting.social == Social.DOUYIN:
            self._setting.type_download = TypeDownloadDoyin.ALL
        else:
            self._setting.type_download = TypeDownloadYoutube.VIDEO_HIGHTQUATITY
        
        if self.rdCustomTime.isChecked():
            self._setting.from_date = datetime.strptime(self.txtFromDate.text(), "%d/%m/%Y") 
            self._setting.to_date = datetime.strptime(self.txtToDate.text(), "%d/%m/%Y") 
        elif self.rdDownloadWeek.isChecked():
            self._setting.from_date = datetime.now() - timedelta(days=7)
            self._setting.to_date = datetime.now()
        elif self.rdDownloadDate.isChecked():
            self._setting.from_date = datetime.now() - timedelta(days=1)
            self._setting.to_date = datetime.now()
        else:
            self._setting.from_date = None
            self._setting.to_date = None
        if self.rdFullChannel.isChecked():
            if self.rdDownloadAllVideo.isChecked():
                self._setting.count = -1
            else:
                self._setting.count = int(self.txtQuatityDownload.text())
            
        self._setting.download_folder = self.txtFolderSaveVideo.text()

        
    
    def processDownload(self,status, message):
        if status == Status.PROCESS_DOWNLOAD_VIDEO:
            print(message)
        if status == Status.START_GET_INFO:
            print(message)
        if status == Status.START_DOWNLOAD_ONE_VIDEO:
            print(message)
        if status == Status.START_DOWNLOAD_LIST_VIDEO:
            print(message)
        if status == Status.DONE_DOWNLOAD_LIST_VIDEO:
            print(message)
        if status == Status.DONE_DOWNLOAD_ONE_VIDEO:
            print(message)
        if status == Status.DONE_GET_INFO:
            print(message)
    def setupButtonRunClick(self):
        self.btnRun.clicked.connect(self.onRunClick)

    def onRunClick(self,event):
        self.dialogProcess.show_overlay()
        # if not self.validateInputSetting():
        #     return
        # try:
        #     self.setupValueSetting()
        # except:
        #     return
        # os.makedirs(self._setting.download_folder, exist_ok=True)
        # socialThread = SocialThread(self._setting)
        # socialThread.process.connect(self.processDownload)
        # socialThread.start()
        
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
        self.loadUiSetting()

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
        self.loadUiSetting()
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
            pixmap = QPixmap("ui/img/DouyinChar.png") 
            self.lbLogoSocial.setPixmap(pixmap)
            self.txtUrl.setPlaceholderText("https://www.douyin.com/user/...")
            self.rdDownloadOld.setEnabled(False)
            self.rdDownloadOld.setChecked(False)
            
        if self._isClick == self.btnYoutube:
            self._setting.social = Social.YOUTUBE
            pixmap = QPixmap("ui/img/YoutubeChart.png") 
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

    def loadUiSetting(self):
        if self._setting.social == Social.DOUYIN:
            self.layouYoutubeType.hide()
            if self.rdDownloadFromLink.isChecked():
                self.layoutOrder.hide()
                self.lauoutQuantity.hide()
            else:
                self.layoutOrder.show()
                self.lauoutQuantity.show()
        else:
            self.layouYoutubeType.show()
            if self.rdDownloadFromLink.isChecked():
                self.layoutOrder.hide()
                self.lauoutQuantity.hide()
            else:
                self.layoutOrder.show()
                self.lauoutQuantity.show()
            

    def setAndRun(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(150, 50)
        self.setupNavigator()
        self.setupShadowsForTheme()
        self.setupGroupCheckbox()
        self.setupCalendar()
        self.setupCountDownload()
        self.setupFolderSelect()
        self.setupButtonRunClick()
        controller.setShadows(self,self.btnDouyin)
        self._isClick = self.btnDouyin
        self._setting.social = Social.DOUYIN
        self._setting.type_id = TypeID.LINK
        self._setting.type_channel = TypeChannel.VIDEO
        self._setting.order_type = OrderType.NEW
        self.loadUiSetting()
        self.show()
