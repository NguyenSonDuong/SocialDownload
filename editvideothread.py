import common.helper as helper
from PyQt5.QtCore import QThread, pyqtSignal
from editvideo.editvideo import EditVideo
class EditVideoThread(QThread):
    process = pyqtSignal(str, dict)
    def __init__(self, path ,setting):
        super().__init__()
        self.setting = setting
        self.path = path
        
    def RunEditVideo(self):
        for path_video in self.path:
            editvideo = EditVideo(setting=self.setting,process=self.process.emit)
            editvideo.run(path_video)

    def run(self):
        if not self.setting :
            raise ValueError("Cấu hình bị lỗi vui lòng cấu hình lại")
            
        self.RunEditVideo()