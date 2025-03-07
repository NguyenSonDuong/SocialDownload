from youtube.youtube import Youtube as yt
from config.setting import Setting, TypeDownloadYoutube, TypeID,Social
import common.helper as helper
from PyQt5.QtCore import QThread, pyqtSignal
from douyin.douyin import Douyin as dy

class SocialThread(QThread):
    process = pyqtSignal(int, dict)
    def __init__(self, setting):
        self.setting = setting
    
    def RunYoutube(self):
        youtube = yt(process=self.process.emit,setting=self.setting)
        youtube.run()

    def RunDouyin(self):
        douyin = dy(process=self.process.emit,setting=self.setting)
        douyin.run()

    def run(self):
        if not self.setting :
            raise Exception("Cấu hình bị lỗi vui lòng cấu hình lại")
        if not self.setting.validate():
            raise Exception("Thiếu các thông tin cần thiết vui lòng thêm các thông tin")
        try:
            if self.setting.social == Social.YOUTUBE:
                self.RunYoutube()
            if self.setting.social == Social.YOUTUBE:
                self.RunDouyin()
        except Exception as ex:
            print(ex)