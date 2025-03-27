import common.helper as helper
from PyQt5.QtCore import QThread, pyqtSignal
from config.setting import Setting, TypeDownloadYoutube, TypeID,Social
from youtube.youtube import Youtube as yt
from douyin.douyin import Douyin as dy
from weibo.weibo import Weibo as wb
class SocialThread(QThread):
    process = pyqtSignal(str, dict)
    def __init__(self, setting):
        super().__init__()
        self.setting = setting
    
    def RunYoutube(self):
        youtube = yt(process=self.process.emit,setting=self.setting)
        youtube.run()

    def RunDouyin(self):
        douyin = dy(process=self.process.emit,setting=self.setting)
        douyin.run()
        
    def RunWeibo(self):
        weibo = wb(process=self.process.emit,setting=self.setting)
        weibo.run()

    def run(self):
        if not self.setting :
            self.process.emit("error",{
                "status": -1,
                "message":"Eroor"
            })
            return
        if not self.setting.validate():
            self.process.emit("error", {
                "status": -1,
                "message": "Eroor"
            })
            return
        try:
            if self.setting.social == Social.YOUTUBE:
                self.RunYoutube()
            if self.setting.social == Social.DOUYIN:
                self.RunDouyin()
            if self.setting.social == Social.WEIBO:
                self.RunWeibo()
        except Exception as ex:
            raise ex