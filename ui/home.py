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
from common.status import Status
import os
from ui.dialog import DialogOverlay
from common.globalstate import GlobalStatePause,GlobalStateRun
from editvideo.setting import EditSetting, EditFrame,EditCut,EditSpeed, EditVideoSetting, EditAudioSetting,EditColorSetting
import pickle
from pprint import pprint
from editvideothread import EditVideoThread

class Ui_HomeWindow(QMainWindow):

    _isClick = None
    _setting = Setting()
    _settingEdit = EditSetting()

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/home.ui",self)
        if not self._settingEdit.edit_video:
            self._settingEdit.edit_video = EditVideoSetting()
        if not self._settingEdit.edit_color:
            self._settingEdit.edit_color = EditColorSetting()
        if not self._settingEdit.edit_audio:
            self._settingEdit.edit_audio = EditAudioSetting()
        self.loadSetting()
        self.socialThread = None
        self.editThread = None
        self.dialogProcess = DialogOverlay(self)
        self.setAndRun()
        self.dialogProcess.hide_overlay()
        self.dialogProcess.setOverlayGeometry(self.centralwidget) 
        self.isRun = GlobalStateRun()
        self.isPause = GlobalStatePause()
        
        
    
    # XỬ lý sự kiện click nút RUN
    
    # lưu và reset settting edit
    
    def loadSetting(self):
        try:
            if os.path.exists("edit.pkl"):
                with open("edit.pkl", "rb") as file:
                    self._settingEdit.edit_video = pickle.load(file)
            if os.path.exists("color.pkl"):
                with open("color.pkl", "rb") as file:
                    self._settingEdit.edit_color = pickle.load(file)
            if os.path.exists("audio.pkl"):
                with open("audio.pkl", "rb") as file:
                    self._settingEdit.edit_audio = pickle.load(file)
        except Exception as e:
            print(e)
                
    def setupSettingFromFile(self):
        if self.groupFrame.button(self._settingEdit.edit_video.edit_frame):
            self.groupFrame.button(self._settingEdit.edit_video.edit_frame).setChecked(True)
        if self.groupSpeed.button(self._settingEdit.edit_video.speed):
            self.groupSpeed.button(self._settingEdit.edit_video.speed).setChecked(True)
        if self.groupCut.button(self._settingEdit.edit_video.cut):
            self.groupCut.button(self._settingEdit.edit_video.cut).setChecked(True)
        if self._settingEdit.edit_video.cut == EditCut.CUT_BASE:
            self.txtSppedCustom.setText(f"{self._settingEdit.edit_video.speed_custom}" if self._settingEdit.edit_video.speed_custom >0 else "")
            self.txtSppedCustom.setEnabled(True)
        else:
            self.txtSppedCustom.setText("")
            self.txtSppedCustom.setEnabled(False)
        if self._settingEdit.edit_video.speed == EditSpeed.SPEED_CUSTOM:
            self.txtCutStart.setText(f"{self._settingEdit.edit_video.cut_start}" if self._settingEdit.edit_video.cut_start >0 else "")
            self.txtCutEnd.setText(f"{self._settingEdit.edit_video.cut_end}" if self._settingEdit.edit_video.cut_end >0 else "")
            self.txtCutStart.setEnabled(True)
            self.txtCutEnd.setEnabled(True)
        else:
            self.txtCutStart.setText("")
            self.txtCutEnd.setText("")
            self.txtCutStart.setEnabled(False)
            self.txtCutEnd.setEnabled(False)
        self.txtFolderSave.setText(self._settingEdit.edit_video.folder_save if self._settingEdit.edit_video.folder_save  else "")
        self.txtInto.setText(f"{self._settingEdit.edit_video.intro}" if self._settingEdit.edit_video.intro else "")
        self.txtOutro.setText(f"{self._settingEdit.edit_video.outro}" if self._settingEdit.edit_video.outro else "")
        self.txtRowVideoTop.setText(f"{self._settingEdit.edit_video.video_up}" if self._settingEdit.edit_video.video_up  else "")
        self.txtRowVideoDown.setText(f"{self._settingEdit.edit_video.video_down}" if self._settingEdit.edit_video.video_down  else "")
        self.txtColumLeft.setText(f"{self._settingEdit.edit_video.video_left}" if self._settingEdit.edit_video.video_left  else "")
        self.txtColumRight.setText(f"{self._settingEdit.edit_video.video_right}" if self._settingEdit.edit_video.video_right  else "")
        
        
        self.txtOpacity.setText(f"{self._settingEdit.edit_color.opacity}" if self._settingEdit.edit_color.opacity >0 else "")
        self.txtRed.setText(f"{self._settingEdit.edit_color.red}" if self._settingEdit.edit_color.red >0 else "")
        self.txtGreen.setText(f"{self._settingEdit.edit_color.green}" if self._settingEdit.edit_color.green >0 else "")
        self.txtBlue.setText(f"{self._settingEdit.edit_color.blue}" if self._settingEdit.edit_color.blue >0 else "")
        self.txtBrightness.setText(f"{self._settingEdit.edit_color.brightness}" if self._settingEdit.edit_color.brightness >0 else "")
        self.txtColorCustom.setText(f"{self._settingEdit.edit_color.custom_color}" if self._settingEdit.edit_color.custom_color >0 else "")
        self.txtSatuation.setText(f"{self._settingEdit.edit_color.saturation}" if self._settingEdit.edit_color.saturation >0 else "")
        self.txtGamma.setText(f"{self._settingEdit.edit_color.gamma}" if self._settingEdit.edit_color.gamma >0 else "")
        self.txtHue.setText(f"{self._settingEdit.edit_color.hue}" if self._settingEdit.edit_color.hue >0 else "")
        
        
    
    def resetSetting(self, type_edit):
        if type_edit == "edit":
            self._settingEdit.edit_video = EditVideoSetting()
            
            self.rdFrameNoChange.setChecked(True)
            self.rdSpeedKeep.setChecked(True)
            self.rgCutNoChange.setChecked(True)
            
            self.txtSppedCustom.setText("")
            self.txtCutStart.setText("")
            self.txtCutEnd.setText("")
            
            self.txtFolderSave.setText("")
            self.txtInto.setText("")
            self.txtOutro.setText("")
            self.txtRowVideoTop.setText("")
            self.txtRowVideoDown.setText("")
            self.txtColumLeft.setText("")
            self.txtColumRight.setText("")
        
        if type_edit == "color":
            self._settingEdit.edit_color = EditColorSetting()
            
            self.txtOpacity.setText("")
            self.txtRed.setText("")
            self.txtGreen.setText("")
            self.txtBlue.setText("")
            self.txtBrightness.setText("")
            self.txtColorCustom.setText("")
            
            self.txtSatuation.setText("")
            self.txtGamma.setText("")
            self.txtHue.setText("")
            self.txtAudioTone_2.setText("")
        
        if type_edit == "audio":
            self._settingEdit.edit_audio = EditAudioSetting()
            
            self.txtMainVolum.setText("")
            self.txtAudioTone.setText("")
            
            self.sliderEditVolum.setValue(50)
            self.txtFolderMusicVideo.setText("")
            
            self.txtEditAudio.setText("")
            
            self.txtFadeIn.setText("")
            self.txtFadeOut.setText("")
            
            self.sliderAudioEdit.setValue(50)
            self.slideFadeIn.setValue(50)
            self.slideFadeOut.setValue(50)
        
    def saveSetting(self,type_id):
        try:
            self._settingEdit.edit_video.edit_frame = self.groupFrame.checkedId()
            
            self._settingEdit.edit_video.speed = self.groupSpeed.checkedId()
            self._settingEdit.edit_video.speed_custom = int(self.txtSppedCustom.text() if self.txtSppedCustom.text() else "-1")
            
            self._settingEdit.edit_video.cut = self.groupCut.checkedId()
            self._settingEdit.edit_video.cut_start = int(self.txtCutStart.text() if self.txtCutStart.text() else "-1")
            self._settingEdit.edit_video.cut_end = int(self.txtCutEnd.text()  if self.txtCutEnd.text() else "-1")
            
            self._settingEdit.edit_video.folder_save = self.txtFolderSave.text()
            self._settingEdit.edit_video.intro = self.txtInto.text()
            self._settingEdit.edit_video.outro = self.txtOutro.text()
            self._settingEdit.edit_video.video_up = self.txtRowVideoTop.text()
            self._settingEdit.edit_video.video_down = self.txtRowVideoDown.text()
            self._settingEdit.edit_video.video_left = self.txtColumLeft.text()
            self._settingEdit.edit_video.video_right = self.txtColumRight.text()
            
            self._settingEdit.edit_color.opacity =  float(self.txtOpacity.text() if self.txtOpacity.text() else "-1")
            
            self._settingEdit.edit_color.red = float(self.txtRed.text() if self.txtRed.text() else "-1")
            self._settingEdit.edit_color.green = float(self.txtGreen.text() if self.txtGreen.text() else "-1")
            self._settingEdit.edit_color.blue = float(self.txtBlue.text() if self.txtBlue.text() else "-1")
            self._settingEdit.edit_color.brightness = float(self.txtBrightness.text() if self.txtBrightness.text() else "-1")
            self._settingEdit.edit_color.custom_color = float(self.txtColorCustom.text() if self.txtColorCustom.text() else "-1")
            
            self._settingEdit.edit_color.saturation = float(self.txtSatuation.text() if self.txtSatuation.text() else "-1")
            self._settingEdit.edit_color.gamma = float(self.txtGamma.text() if self.txtGamma.text() else "-1")
            self._settingEdit.edit_color.hue = float(self.txtHue.text() if self.txtHue.text() else "-1")
            # self._settingEdit.edit_color. = int(self.txtOpacity.text() if self.txtOpacity.text() else "-1")
        except Exception as ex:
            QMessageBox.information(self,"Cảnh báo","Lỗi định dạng dữ liệu")
            return
        
        # if self.groupSpeed.button(self._settingEdit.edit_video.speed):
        #     self.groupSpeed.button(self._settingEdit.edit_video.speed).setChecked(True)
        # if self.groupCut.button(self._settingEdit.edit_video.cut):
        #     self.groupCut.button(self._settingEdit.edit_video.cut).setChecked(True)
        
        
        with open(f"{type_id}.pkl", "wb") as file:
            if type_id == "edit":
                pickle.dump(self._settingEdit.edit_video, file)
            if type_id == "color":
                pickle.dump(self._settingEdit.edit_color, file)
            # if type_id == "audio":
            #     pickle.dump(self._settingEdit.edit_audio, file)
    
    # cài xử lý tải video
    
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
        if status == Status.START_GET_INFO:
            self.dialogProcess.log(message["message"],"blue")
        if status == Status.PROCESS_GET_INFO:
            self.dialogProcess.log(message["message"],"blue")
        if status == Status.DONE_GET_INFO:
            self.dialogProcess.log(message["message"],"green")
            
        if status == Status.START_DOWNLOAD_ONE_VIDEO:
            self.dialogProcess.log(message["message"],"blue")
        if status == Status.PROCESS_DOWNLOAD_ONE_VIDEO:
            self.dialogProcess.frame.lbTienTrinhPhu.setText("Đang tải video...")
            self.dialogProcess.setProcessPhu(message["message"]["percent"],100)
        if status == Status.DONE_DOWNLOAD_ONE_VIDEO:
            self.dialogProcess.setProcess((message["message"]["success"] + message["message"]["error"]),message["message"]["total"])
            
        if status == Status.START_DOWNLOAD_LIST_VIDEO:
            self.dialogProcess.log(message["message"],"blue")
        if status == Status.DONE_DOWNLOAD_LIST_VIDEO:
            self.dialogProcess.log(message["message"],"green")
        if status == Status.PROCESS_DOWNLOAD_LIST_VIDEO:
            self.dialogProcess.log(message["message"],"black")
            
        if status == Status.ERROR_GET_INFO:
            self.dialogProcess.log(message["message"],"red")
        if status == Status.ERROR_DOWNLOAD_ONE_VIDEO:
            self.dialogProcess.log(message["message"],"red")
        if status == Status.ERROR_DOWNLOAD_LIST_VIDEO:
            self.dialogProcess.log(message["message"],"red")
            
        if status == Status.DONE:

            if self.rdDownloadWithEdit.isChecked():
                self.dialogProcess.log("Bắt đầu chỉnh sửa theo cài đặt: ","green")
                if self.txtFolderSaveVideo.text() and self.txtFolderSaveVideo.text() != "":
                    self._setting.download_folder = self.txtFolderSaveVideo.text()
                    self.runEditVideo()
                else:
                    QMessageBox.information(self, "Cảnh báo", "Vui lòng nhập folder video nguồn")
            else:
                self.isRun.set_value(False)
                self.isPause.set_value(False)
                self.dialogProcess.log(message["message"], "green")
                self.dialogProcess.hide_overlay()
        if status == Status.PAUSE:
            self.dialogProcess.log(message["message"],"yellow")
        if status == Status.ERROR:
            self.dialogProcess.log(message["message"],"red")
    def onProcessEdit(self,status,message):
        if status == "save_video":
            self.dialogProcess.frame.lbTienTrinhPhu.setText("Đang lưu video sau chỉnh sửa...")
            self.dialogProcess.setProcessPhu(message["message"]["percent"],100)
        elif status == "error":
            self.dialogProcess.log(message["message"]["message"],"red")
        else:
            self.dialogProcess.log(message["message"],"blue" if message["status"] == 1 else "green" if message["status"] == 2 else "red")
            if message["status"] == 5:
                self.dialogProcess.hide_overlay()
                self.isRun.set_value(False)
                self.isPause.set_value(False)
                self.dialogProcess.log(message["message"], "green")
    def setupButtonRunClick(self):
        self.btnRun.clicked.connect(self.onRunClick)

    def onRunClick(self,event):
        try:
            if self.rdDownloadWithoutEdit.isChecked() or self.rdDownloadWithEdit.isChecked():
                if not self.validateInputSetting():
                    return
                try:
                    self.setupValueSetting()
                except:
                    return
                os.makedirs(self._setting.download_folder, exist_ok=True)
                if not self.isRun.get_value():
                    self.isRun.set_value(True)
                    self.isPause.set_value(False)
                    if self.socialThread and self.socialThread.isRunning():
                        self.socialThread.quit()
                        self.socialThread.wait()
                    self.socialThread = SocialThread(self._setting)
                    self.socialThread.process.connect(self.processDownload)
                    self.socialThread.start()
                else:
                    QMessageBox.information(self, "Cảnh báo", "Có tiến trình đang chạy vui lòng chờ tiến trình chạy hêt")

                self.dialogProcess.show_overlay()
            else:
                if not self.isRun.get_value():
                    self.isRun.set_value(True)
                    self.isPause.set_value(False)
                # self.dialogProcess.log("Bắt đầu chỉnh sửa theo cài đặt: ","green")
                    if self.txtFolderSaveVideo.text() and self.txtFolderSaveVideo.text() != "":
                        self._setting.download_folder = self.txtFolderSaveVideo.text()
                        self.runEditVideo()
                        self.dialogProcess.show_overlay()
                    else:
                        QMessageBox.information(self,"Cảnh báo","Vui lòng nhập folder video nguồn")
                else:
                    QMessageBox.information(self, "Cảnh báo", "Có tiến trình đang chạy vui lòng chờ tiến trình chạy hêt")
                    self.dialogProcess.show_overlay()

        except Exception as e:
            QMessageBox.information(self, "Cảnh báo", f"Lỗi: {e}")
    def runEditVideo(self):
        from os import walk
        file_list = []
        file_list_path = []
        for (dirpath, dirnames, filenames) in walk(self._setting.download_folder):
            file_list.extend(filenames)
            for item in file_list:
                file_list_path.append(f"{dirpath}/{item}")
            break
        if not file_list or len(file_list) <= 0:
            QMessageBox.information(self, "Cảnh báo", "Thư mục không có video mong kiểm tra lại")
        if self.editThread and self.editThread.isRunning():
            self.editThread.quit()
            self.editThread.wait()
        self.editThread = EditVideoThread(file_list_path, self._settingEdit)
        self.editThread.process.connect(self.onProcessEdit)
        self.editThread.start()
    # xử lý Group radiobutom
    
    # Phần cài đặt cho edit video
    def setupGroupCheckBoxEditVideo(self):
        self.groupFrame = QButtonGroup(self)
        self.groupFrame.setExclusive(True)
        self.groupFrame.addButton(self.rdFrameNoChange,0)
        self.groupFrame.addButton(self.rd169,1)
        self.groupFrame.addButton(self.rd619,2)
        self.groupFrame.addButton(self.rd43,3)
        
        self.groupSpeed = QButtonGroup(self)
        self.groupSpeed.setExclusive(True)
        self.groupSpeed.addButton(self.rdSpeedKeep,0)
        self.groupSpeed.addButton(self.rdSpeedx2,1)
        self.groupSpeed.addButton(self.rdSpeedx4,2)
        self.groupSpeed.addButton(self.rdCustomSpeed,3)
        
        self.groupCut = QButtonGroup(self)
        self.groupCut.setExclusive(True)
        self.groupCut.addButton(self.rgCutNoChange,0)
        self.groupCut.addButton(self.rdCut3sStart,1)
        self.groupCut.addButton(self.rdCut3sEnd,2)
        self.groupCut.addButton(self.rdCut1sForeach5s,3)
        self.groupCut.addButton(self.rdSpeedCustom,4)
        
        self.groupFrame.buttonClicked.connect(self.onSelectFrame)
        self.groupSpeed.buttonClicked.connect(self.onSelectSpeed)
        self.groupCut.buttonClicked.connect(self.onSelectCut)
        
        self.btnSaveEditVideo.clicked.connect(self.onBtnSaveEditVideoClick)
        self.btnEditColorVideo.clicked.connect(self.onBtnEditColorVideoClick)
        self.btnSaveAudioSetting.clicked.connect(self.onBtnSaveAudioSettingClick)
        
        self.btnResetEditVideo.clicked.connect(self.onBtnResetEditVideoClick)
        self.btnEditColorReset.clicked.connect(self.onBtnEditColorResetClick)
        self.btnResetAudioSetting.clicked.connect(self.onBtnResetAudioSettingClick)
    
    def onBtnResetEditVideoClick(self, event):
        self.resetSetting("edit")
    def onBtnEditColorResetClick(self, event):
        self.resetSetting("color")
    def onBtnResetAudioSettingClick(self, event):
        self.resetSetting("audio")
    
    def onBtnSaveEditVideoClick(self, event):
        self.saveSetting("edit")
    def onBtnEditColorVideoClick(self, event):
        self.saveSetting("color")
    def onBtnSaveAudioSettingClick(self, event):
        self.saveSetting("audio")
    
    def onSelectFrame(self, button):
        button_id = self.groupFrame.id(button)  
        self._settingEdit.edit_video.edit_frame = button_id
        
    def onSelectSpeed(self, button):
        button_id = self.groupSpeed.id(button)  
        self._settingEdit.edit_video.speed = button_id
        if button_id == EditSpeed.SPEED_BASE:
            self.txtSppedCustom.setEnabled(False)
        if button_id == 1:
            self._settingEdit.edit_video.speed_custom = 2
            self.txtSppedCustom.setEnabled(False)
        if button_id == 2:
            self._settingEdit.edit_video.speed_custom = 4
            self.txtSppedCustom.setEnabled(False)
        if button_id == EditSpeed.SPEED_CUSTOM:
            self.txtSppedCustom.setEnabled(True)
        
    
        
    def onSelectCut(self, button):
        button_id = self.groupCut.id(button)  
        self._settingEdit.edit_video = EditVideoSetting()
        self._settingEdit.edit_video.speed = button_id
        if (button_id == EditCut.CUT_BASE or button_id == EditCut.CUT_FOREARCH):
            self.txtCutStart.setEnabled(False)
            self.txtCutEnd.setEnabled(False)
        if (button_id ==1):
            self._settingEdit.edit_video.cut_start = 3
            self.txtCutStart.setEnabled(False)
            self.txtCutEnd.setEnabled(False)
        if (button_id ==2):
            self._settingEdit.edit_video.cut_end = 3
            self.txtCutStart.setEnabled(False)
            self.txtCutEnd.setEnabled(False)
        if (button_id ==4):
            self.txtCutStart.setEnabled(True)
            self.txtCutEnd.setEnabled(True)
        
        
            
        
    
    # phần cài đặt cho download video
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
        
        
      
    
    def onFolderSaveClick(self,event):
        folder_path = QFileDialog.getExistingDirectory(self, "Chọn thư mục", "D:/")
        
        if folder_path:  # Nếu người dùng chọn thư mục
            self.txtFolderSave.setText(f"{folder_path}")
       
    def onSelectIntro(self,event):
        folder_path, _ = QFileDialog.getOpenFileName(self, "Chọn thư mục", "D:/")
        
        if folder_path:  # Nếu người dùng chọn thư mục
            self.txtInto.setText(f"{folder_path}")
            
    def onSelectOutro(self,event):
        folder_path, _ = QFileDialog.getOpenFileName(self, "Chọn thư mục", "D:/")
        
        if folder_path:  # Nếu người dùng chọn thư mục
            self.txtOutro.setText(f"{folder_path}")
            
    def onSelectUpVideo(self,event):
        folder_path, _ = QFileDialog.getOpenFileName(self, "Chọn thư mục", "D:/")
        
        if folder_path:  # Nếu người dùng chọn thư mục
            self.txtRowVideoTop.setText(f"{folder_path}")
            
    def onSelectDownVideo(self,event):
        folder_path, _ = QFileDialog.getOpenFileName(self, "Chọn thư mục", "D:/")
        
        if folder_path:  # Nếu người dùng chọn thư mục
            self.txtRowVideoDown.setText(f"{folder_path}")
            
    def onSelectLeftVideo(self,event):
        folder_path, _ = QFileDialog.getOpenFileName(self, "Chọn thư mục", "D:/")
        
        if folder_path:  # Nếu người dùng chọn thư mục
            self.txtColumLeft.setText(f"{folder_path}")
            
            
    def onSelectRightVideo(self,event):
        folder_path, _ = QFileDialog.getOpenFileName(self, "Chọn thư mục", "D:/")
        
        if folder_path:  # Nếu người dùng chọn thư mục
            self.txtColumRight.setText(f"{folder_path}")
    
    
            

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
        self.setupGroupCheckBoxEditVideo()
        self.setupSettingFromFile()
        controller.setShadows(self,self.btnDouyin)
        self._isClick = self.btnDouyin
        self._setting.social = Social.DOUYIN
        self._setting.type_id = TypeID.LINK
        self._setting.type_channel = TypeChannel.VIDEO
        self._setting.order_type = OrderType.NEW
        self.loadUiSetting()
        self.show()
        self.btnClose.clicked.connect(self.onCloseClick)
        self.btnMinimize.clicked.connect(self.onMinimize)
        self.btnSelectFolderSaveEdit.clicked.connect(self.onFolderSaveClick)
        self.btnSelectLeftVideo.clicked.connect(self.onSelectLeftVideo)
        self.btnSelectIntro.clicked.connect(self.onSelectIntro)
        self.btnSelectOutro.clicked.connect(self.onSelectOutro)
        
        self.btnSelectUpVideo.clicked.connect(self.onSelectUpVideo)
        self.btnSelectDownVideo.clicked.connect(self.onSelectDownVideo)
        
        
        self.btnSelectRightVideo.clicked.connect(self.onSelectRightVideo)
        self.btnEditVideo.clicked.connect(self.onEditVideoClick)
        self.btnEditColor.clicked.connect(self.onBtnEditColorClick)
        self.btnEditAudio.clicked.connect(self.onBtnEditAudioClick)

    def onEditVideoClick(self,event):
        if self.editMainLayout.isHidden():
            self.editMainLayout.show()
        else:
            self.editMainLayout.hide()
    def onBtnEditColorClick(self,event):
        if self.editColorMainLayout.isHidden():
            self.editColorMainLayout.show()
        else:
            self.editColorMainLayout.hide()
    def onBtnEditAudioClick(self,event):
        if self.editAudioMainLayout.isHidden():
            self.editAudioMainLayout.show()
        else:
            self.editAudioMainLayout.hide()
    
    def onCloseClick(self, event):
        self.close()
    def onMinimize(self, event):
        self.showMinimized()
