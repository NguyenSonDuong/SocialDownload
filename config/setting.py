from dataclasses import dataclass
from datetime import datetime

class TypeID:
    CHANNEL_SHORT =1
    CHANNEL_VIDEO =2
    VIDEO = 3
    SHORT = 4
    DOUYIN_LINK = 5
    DOUYIN_USER = 6
    

class Social:
    YOUTUBE = 0
    DOUYIN = 1
    WEIBO = 2
    TWITTER = 3

class TypeDownloadYoutube:
    VIDEO_HIGHTQUATITY = "bestvideo[ext=mp4]+bestaudio[ext=m4a]"
    VIDEO_BEST = "bestvideo[ext=mp4]"
    AUDIO_BEST = "bestaudio[ext=m4a]"
    VIDEO_WORST = "worstvideo[ext=mp4]"
    AUDIO_WORST = "worstaudio[ext=m4a]"
    
class TypeDownloadDoyin:
    ALL = "all"
    VIDEO = "video"
    IMAGE = "image"
    
@dataclass
class Setting:
    social: int = -1
    download_folder: str = None
    id: str = None
    type_id: int = -1
    type_download: str = None
    from_date: datetime = None
    to_date: datetime = None
    count: int = -1

    def validate(self):
        if self.social < 0 or self.social > Social.TWITTER:
            return False
        if not self.download_folder or self.download_folder == "":
            return False
        if not self.id:
            return False
        if self.type_id < 0:
            return False
        if not self.type_download:
            return False
        import common.helper as helper
        helper.checkDirAndCreate(self.download_folder)
        return True