from PyQt5 import uic
from PyQt5.QtGui import QColor, QPainter, QColor,QTextCharFormat, QTextCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtWidgets import  QMainWindow, QMessageBox, QFileDialog
from config.setting import Setting,OrderType,TypeChannel,TypeDownloadDoyin,TypeDownloadYoutube,Social,TypeID
from social import SocialThread
from common.status import Status
from common.globalstate import GlobalStatePause,GlobalStateRun
import common.uicontroller as controller
import os
import json
class DownloadView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUIUX()
        
    def setUIUX(self):
        uic.loadUi("ui/download2.ui",self)
        self.show()
        
        self.isRun = GlobalStateRun()
        self.isPause = GlobalStatePause()
        
        self.btnDownload.clicked.connect(self.onBtnDownloadClicked)
        self.btnSelectFolder.clicked.connect(self.onBtnSelectFolderClicked)
        self.btnStop.clicked.connect(self.onBtnStopClicked)
        self.btnPause.clicked.connect(self.onBtnPauseClicked)
        
    def onBtnStopClicked(self,event):
        self.isRun.set_value(False)
        
    def onBtnPauseClicked(self,event):
        self.isPause.set_value(True)
        
    def onBtnDownloadClicked(self,event):
        if not self.validateInput():
            return
        if not self.isRun.get_value():
            self.isRun.set_value(True)
            self.isPause.set_value(False)
            setting = Setting()
            
            setting.social = self.cbbSocial.currentIndex()
            setting.download_folder = self.txtFolderSave.text()
            setting.type_channel = self.cbbTypeLink.currentText()
            
            if self.cbAll.isChecked():
                setting.count = -1
            else:
                setting.count = int(self.txtQuantity.text())

            if setting.social == Social.YOUTUBE:
                setting.type_download = self.cbbQuatity.currentText()
            else:
                setting.type_download = self.cbbTypeDownloadDouyin.currentText()
            setting.type_id = self.cbbTypeLink.currentIndex()
            
            if setting.social == Social.YOUTUBE:
                setting.id = controller.validateUrlYoutube(self.txtUrl.text(),setting)
            elif setting.social == Social.DOUYIN:
                setting.id = controller.validateUrlDouyin(self.txtUrl.text(),setting)
            elif setting.social == Social.WEIBO:
                setting.id = controller.validateUrlWeibo(self.txtUrl.text())  
            if not setting.id or setting.id == "":
                QMessageBox.information(self,"Cảnh báo","Sai định dạng link vui lòng kiểm tra mạng xã hội và cách tải")
                self.isRun.set_value(False)
                self.isPause.set_value(False)
                return
            os.makedirs(setting.download_folder, exist_ok=True)
            self.socialThread = SocialThread(setting)
            self.socialThread.process.connect(self.processDownload)
            self.socialThread.start()
    
    def validateInput(self):
        if not self.txtUrl.text() or self.txtUrl.text() == "":
            QMessageBox.information(self,"Cảnh báo","Vui lòng nhập link")
            return False
        if not self.txtFolderSave.text() or self.txtFolderSave.text() == "":
            QMessageBox.information(self,"Cảnh báo","Vui lòng lựa chọn đường dẫn lưu File")
            return False
        try:
            if not self.cbAll.isChecked():
                inputA = int(self.txtQuantity.text())
        except:
            QMessageBox.information(self,"Cảnh báo","Vui lòng nhập số lượng dạng số")
            return False
        return True
        
        
    
    def onBtnSelectFolderClicked(self,event):
        folder_path = QFileDialog.getExistingDirectory(self, "Chọn thư mục", "E:/")
        
        if folder_path:  # Nếu người dùng chọn thư mục
            self.txtFolderSave.setText(f"{folder_path}")
            
    def append_text(self, text, color):
        """ Thêm văn bản với màu tùy chỉnh """
        cursor = self.txtLog.textCursor()  
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))  

        cursor.movePosition(QTextCursor.End) 
        cursor.mergeCharFormat(fmt)  
        cursor.insertText(text + "\n")   
        
    def processDownload(self,status, message):
        if status == Status.START_GET_INFO:
            self.append_text(message["message"],"blue")
        if status == Status.PROCESS_GET_INFO:
            self.append_text(json.dumps(message["message"]),"blue")
        if status == Status.DONE_GET_INFO:
            self.append_text(message["message"],"green")
            
        if status == Status.START_DOWNLOAD_ONE_VIDEO:
            self.append_text(message["message"],"blue")
        if status == Status.PROCESS_DOWNLOAD_ONE_VIDEO:
            self.lbChill.setText("Đang tải video...")
            self.pbChill.setValue(int(message["message"]["percent"]))
            self.pbChill.setMaximum(100)
        if status == Status.DONE_DOWNLOAD_ONE_VIDEO:
            self.pbMain.setValue(int(message["message"]["success"] + message["message"]["error"]))
            self.pbChill.setMaximum(int(message["message"]["total"]))
            
        if status == Status.START_DOWNLOAD_LIST_VIDEO:
            self.append_text(message["message"],"blue")
        if status == Status.DONE_DOWNLOAD_LIST_VIDEO:
            self.append_text(message["message"],"green")
        if status == Status.PROCESS_DOWNLOAD_LIST_VIDEO:
            self.append_text(message["message"],"black")
            
        if status == Status.ERROR_GET_INFO:
            self.append_text(message["message"],"red")
        if status == Status.ERROR_DOWNLOAD_ONE_VIDEO:
            self.append_text(message["message"],"red")
        if status == Status.ERROR_DOWNLOAD_LIST_VIDEO:
            self.append_text(message["message"],"red")
            
        if status == Status.DONE:
            self.append_text("Bắt đầu chỉnh sửa theo cài đặt: ","green")
            self.isRun.set_value(False)
            self.isPause.set_value(False)
        if status == Status.PAUSE:
            self.append_text(message["message"],"yellow")
        if status == Status.ERROR:
            self.append_text(message["message"],"red")
        